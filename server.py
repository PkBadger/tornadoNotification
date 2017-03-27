#importss
import tornado.ioloop
import tornado.web
import json
from tornado import gen, websocket
from tornado.options import define, options, parse_command_line

#------------------------------------#
# Arguments                          #
#------------------------------------#

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

#--------------------------------------#
#  Clients list raspberry and IOS      #
#--------------------------------------#
clientUser = []

#---------------------------------------#
#Socket handler                         #
#---------------------------------------#
class SocketUserHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        print("origin")
        return True

    def open(self):
        print("open")
        if self not in clientUser:
            clientUser.append(self)
        print(clientUser)

    def on_close(self):
        print("on_close")
        if self in clientUser:
            clientUser.remove(self)
        print(clientUser)

#---------------------------------#
# Notification handler            #
#---------------------------------#

class alertHandler(websocket.WebSocketHandler):
    def get(self):
        #http://localhost:8888/alert?id=100
        id = self.get_argument("id")
        data = {"action":"alert","id":id}
        print(data)
        for c in clientUser:
            c.write_message(data)

#--------------------------------------#
# Main function                        #
#--------------------------------------#

def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/socket", SocketUserHandler),
            (r"/alert", alertHandler)
        ],
        xsrf_cookies=True,
        debug=options.debug,
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
