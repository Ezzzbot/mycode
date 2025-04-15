
// load() 函数：加载页面并绑定事件
function load(tool) {
    fetch(`/${tool}`)
        .then(response => {
            if (!response.ok) throw new Error('网络响应异常');
            return response.text();
        })
        .then(data => {
            // 将加载的内容填充到 tool-content 容器中
            document.getElementById('tool-content').innerHTML = data;
            // 聊天
            chat();
        })
        .catch(error => {
            console.error('加载工具内容失败:', error);
            document.getElementById('tool-content').innerHTML = `<p style="color: red;">加载失败，请稍后重试。</p>`;
            alert('加载页面时出现错误，请检查您的网络连接并重试.'); // 用户友好的提示
        });
}
// 发送聊天信息
function chat() {
    const inputForm = document.getElementById('inputForm');
    if (inputForm) {
        inputForm.addEventListener('submit', function(event) {
            event.preventDefault();  // 阻止表单默认提交行为

            const userInput = document.getElementById('user_input').value;
            const messagesContainer = document.getElementById('messages');

            // 提交数据到服务器
            fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `user_input=${encodeURIComponent(userInput)}`
            }).then(response => {
                if (response.ok) {
                    console.log('输入已提交');

                    // 在这里添加用户的输入到消息显示区
                    const messageElement = document.createElement('div');
                    messageElement.classList.add('message');
                    messageElement.textContent = userInput;
                    messagesContainer.appendChild(messageElement);

                    // 清空输入框
                    document.getElementById('user_input').value = '';

                    // 可选：滚动到最新消息处
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                } else {
                    console.error('提交失败');
                }
            }).catch(error => {
                console.error('提交请求失败:', error);
            });
        });
    }
}