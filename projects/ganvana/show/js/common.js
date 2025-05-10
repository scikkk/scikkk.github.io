var common = {
    checkBrowser: function () {
        var browser = {
            appCodeName: navigator.appCodeName,
            appName: navigator.appName,
            appVersion: navigator.appVersion
        }
        // console.log(browser);
        if (browser.appName != 'Netscape') {
            alert('您的浏览器可能不兼容，推荐使用Chrome、Safari、MicroSoft EDGE等现代浏览器')
        }
    },
    alert: function (result, url) {
        // console.log(result, url)
        // 1 判断是否有参数，如果没有不执行
        if (arguments.length == 0) return;
        if (result.length == 0) return;

        var data = {
            domClass: 'alertOK',
            title: null,
            content: null,
            jumpUrl: null
        }
        if (!result[0]) {
            data.domClass = 'alertWrong';
        }
        if (result[1]) {
            data.title = result[1]
        }
        if (result[2]) {
            data.content = result[2]
        }
        if (url) {
            data.jumpUrl = url
        }
        common.doAlert(data, result[0])
    },
    alertX: function (title) {
        var data = {
            domClass: 'alertWrong',
            title: title,
            content: null,
            jumpUrl: null
        }
        common.doAlert(data, false, 5000)
    },
    alertOK: function (title) {
        var data = {
            domClass: 'alertOK',
            title: title,
            content: null,
            jumpUrl: null
        }
        common.doAlert(data, true)
    },
    doAlert: function (data, success, time) {
        if (!time) {
            time = 3000;
        }
        if (!success) {
            time = 5000
        }
        //  判断当前页面是否已经存在#alert元素，如果没有，创建
        if (document.getElementById('alert')) {

        } else {
            $("body").append('<div id="alert"></div>');
        }
        // 提醒标题 title
        var titleHTML = '';
        if (data.title) {
            titleHTML = '<div class="title">' + data.title + '</div>';
        }
        // 4 详细描述 msg
        var contentHTML = '';
        if (data.content) {
            contentHTML = '<div class="content">' + data.content + '</div>';
        }
        // 6 本条消息的id
        data.msgID = 'msg' + new Date().getTime();
        // 7 插入dom
        var dom = '<div class="alert ' + data.domClass + '" id="' + data.msgID + '">' +
            // '<i class="zmdi closeAlert zmdi-close-circle-o zmdi-hc-lg"></i>' +
            titleHTML + contentHTML +
            '</div>';
        $("#alert").append(dom);

        setTimeout(function () {
            $("#" + data.msgID).remove();
            if (data.jumpUrl) {
                if (data.jumpUrl == 'reload') {
                    location.reload();
                }
                else if (data.jumpUrl == 'close') {
                    window.close()
                }
                else {
                    window.location.href = data.jumpUrl;
                }
            }
        }, time)
    },
}

var transJSON = function (key, value) {
    // console.log(value)
    if (typeof (value) === 'string') {
        value = value.replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&bsol;/g, '\\');
    }
    return value
}
