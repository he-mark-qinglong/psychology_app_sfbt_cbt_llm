from app import app  

if __name__ == '__main__':  
    # 为了使用浏览器的语音功能，网站要求必须是https的，所以才添加证书。  
    # 添加证书，当前目录运行：openssl req -x509 -newkey rsa:4096 -nodes -out llm_cert.pem -keyout llm_key.pem -days 365  
    app.run(debug=True, host='0.0.0.0', port=8443, ssl_context=('llm_cert.pem', 'llm_key.pem'))
    