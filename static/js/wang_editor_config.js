 $(document).ready(function () {
            // 创建富文本编辑器元素节点
            var wehtml = "<div id='wangcontent'></div>"
            // 获取div，.form-group是根据实际情况填入的；
            var field_div = document.querySelectorAll(".form-group")
            //插入上面定义的wehtml,field_div[2]定位到第三个class名为.form-group的div；
            field_div[1].insertAdjacentHTML('beforeend', wehtml);
            
 
            const E = window.wangEditor
            const editor = new E("#wangcontent")
            //复用的时候下面的ID需要根据情况修改
            const $text1 = $('#id_content')
            console.log($text1.val())
            editor.config.onchange = function (html) {
                // 第二步，监控变化，同步更新到 textarea
                $text1.val(html)
            }
            editor.config.height = 500
            // 配置 server 接口地址，复用的时候修改
            editor.config.uploadImgServer = '/uploadimage/'
            editor.config.uploadFileName = 'file'
            editor.create()
            editor.txt.html($text1.val())
            // 第一步，初始化 textarea 的值
            $text1.val(editor.txt.html())
            //隐藏原有的输入框
            $text1.attr("style", "display:none")
 })