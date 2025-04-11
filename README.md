**LSEG Stock exchange chatbot**

Project setup:

    pip install flask
    pip install flask-cors
    python app.py
    = Connect to  http://127.0.0.1:5000

Project structure:

    - app.py: Flask backend that handles stock data in a tree structure object, parses user input from frontend and sends the next options
    - templates/index.html: HTML template for the chatbot UI that also includes JavaScript and jQuery scripts to handle functionalities and communication with backend
    - static/style.css: CSS stylesheet for styling the chatbot a bit
    - azure-pipeline.yaml: Azure pipeline to deploy Flask app to an App Service in cloud

For this project, I have chosen Flask for backend and an HTML template with CSS, JS and jQuery for frontend. 

Since it all comes down to having a menu-based chatbot, I have defined an object for the tree-like structure of the stock data in the backend.
Therefore, we could say we have backend orchestration. In the backend, there is a function to handle user input based on the current step and current selection,
some error handling in case of invalid user input and also a function to handle the "back" functionality.

On the frontend side, there is a chatbot header, a footer and the chatbot box where the messages are inserted. Each time, a new div is created dynamically.

Also, there is an Azure pipeline yaml file that can be used to deploy the Flask application to an App Service in cloud, if we have an active subscription in place.

DEMO:

![image](https://github.com/user-attachments/assets/dc0f1ce3-ec8d-46d6-b0a5-56b3428263dd)


