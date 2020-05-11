import frida
import sys

jsCode = """
Java.perform(function(){
    console.log('开始')
    var ClassName = Java.use("com.sankuai.waimai.foundation.utils.security");
    console.log(ClassName.a)
    console.log(this);
    console.log(this.a);
    return this
});
"""
#
#
def message(message, data):
    if message["type"] == 'send':
        print(u"[*] {0}".format(message['payload']))
    else:
        print(message)
#
#
# process = frida.get_remote_device().attach("com.qianyu.demo")
# script = process.create_script(jsCode)
# script.on("message", message)
# script.load()
# sys.stdin.read()

session = frida.get_usb_device().attach('com.sankuai.meituan.takeoutnew')
script = session.create_script(jsCode)
script.load()


# import frida
# rdev = frida.get_remote_device().attach('com.sankuai.meituan.takeoutnew')
# front_app = rdev.get_frontmost_application()
# print(rdev)