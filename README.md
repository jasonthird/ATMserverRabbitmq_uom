# ATM tellel machine server using rabbitMQ
Exercise for the distributed programming course in university of macedonia

## Python3.10.8 dependences 
mariadb(1.1.4), pika(1.3.1)
  
## Usage
Given that you have access to a mariadb instance, modify the sqlConfig.json to configure the database connection.
You will also need to setup a rabbitMQ broker, (change the hostIp veriable inside the main.py file if your broker is not running locally)
<br>
If you are running it for the first time and need to set the database up just run
``` python3 SqlConnection setupDb```. This will automatically connect to mariadb and create and setup a database (name specified in sqlConfig.json) with some test data.
<br>
<br><br>Run ```python3 main.py``` to start the server.

