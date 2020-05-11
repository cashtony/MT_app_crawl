# -*- coding:utf-8 -*-
"""
*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
Author: liyafeng
File Name: frida_hook.py
Create Date: 2020/4/14 19:12
Description : 
*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
"""
import frida
import sys


rmtdv = frida.get_usb_device()
# session = rmtdv.get_frontmost_application()
# print(session)
session = rmtdv.attach("com.sankuai.meituan.takeoutnew")


# message为map，取出key payload 的value
def on_message(message, data):
    print(message)


def hook(jscode):
    script = session.create_script(jscode)
    # 设置message 回调函数为 on_message。js 调用send 就会发到 on_message
    script.on("message", on_message)
    script.load()
    sys.stdin.read()


# HOOK普通方法
jscode0 = """
Java.perform(function () {
    var utils = Java.use('com.bm.wanma.utils.PreferencesUtil');
    utils.getStringPreferences.implementation = function (a, b) {
        console.log("Hook Start...");
        console.log(a);
        console.log(b);
		var num = this.getStringPreferences(a,b);
		console.log("result:", num);
		return num;
    }
    
    var _replace = Java.use("com.bm.wanma.utils.Tools");
    _replace.replace.implementation = function (a) {
        console.log("replace arg1:", a);
		var num1 = this.replace(a);
		console.log("replace result:", num1);
		return num1;
	}
	
	var gdtp = Java.use("com.bm.wanma.net.GetDataPost");
    gdtp.hashMapPutheaders.implementation = function () {
		var rlt = this.hashMapPutheaders();
		console.log("gdtp result:", rlt);
		return rlt;
	}
	
	var rcutil = Java.use("com.bm.wanma.utils.RC4Util");
	var _Array = Java.use("java.util.Arrays");
	rcutil.base64Encode.implementation = function (b) {
    	console.log("b:", _Array.toString(b));
		var brlt = this.base64Encode(b);
		console.log("base64Encode result:", brlt);
		return brlt;
	}
	
});
"""

jscode = """

Java.perform(function () {
	var fragment = Java.use("com.sankuai.waimai.R");
	fragment.implementation = function (a, b, c, d) {
    	console.log("a:", a);
    	console.log("b:", b);
    	console.log("c:", c);
    	console.log("d:", d);
		var rlt = this.requestFordata(a, b);
		console.log("requestFordata result:", rlt);
		return rlt;
	}

});
"""


if __name__ == '__main__':
    hook(jscode)


