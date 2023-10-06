# Register_Website
A secure website where a user can create an account and log in. We built it on a virtual computer running the **CentOS 7** operating system. The database used to hold user data has **MariaDB** as database management system, and the site was built using **HTML and CSS** tools.
## Implemetations
I downloaded the MariaDB database management system with the ``yum install mariadb-server -y`` command, where I later started it with ``sudo systemctl start mariadb``. Below I show what its status is with the ``sudo systemctl status mariadb`` command.
![image](https://github.com/Despoina2000/Register_Website/assets/66719546/1decb473-b0ed-424c-a457-bcb296f322c9)

<br>Then, to create my own server I executed the commands: ``sudo mysql`` and ``CREATE USER 'myserver'@'localhost' IDENTIFIED BY '3180146';``. To have all permissions, I executed the command ``GRANT ALL PRIVILEGES ON *.* TO 'myserver'@'localhost' WITH GRANT OPTION;``. To build the GDPR database I used the command ``CREATE DATABASE GDPR;``. The table ``users`` is for storing the password and the table ``logging`` is for storing informations about the numbers of tryings to log in the page with the wrong password and when was the last date when the password was updated. You can find the rest **SQL** code [here](https://github.com/Despoina2000/Register_Website/blob/main/database/SQL_COMMANDS.mysql).

<br> The data from the table **users** containing the users is displayed below. Because of the code I created to save codes upon registration, the passwords was already encoded.
![image](https://github.com/Despoina2000/Register_Website/assets/66719546/44bdfe72-f17e-431c-b123-1540dc1b2760)

<br> The data from the table **logging**: 
<br>![image](https://github.com/Despoina2000/Register_Website/assets/66719546/73ab9084-99fc-4cca-bda8-84bf71bd6859)



<br> To provide security to our stored database passwords in case of data sniffing, I used the tactic of encrypting them with salt when the user stores them to the registers page. Specifically, I used the python method ``hashlib.pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None)`` in my method ``register()`` which encodes the password with one of the following hash algorithm: **'sha224', 'sha384', 'sha512', 'sha256'**, along with the random salt value, for as many times as desired and with the generate biggest size option. This way the attacker will not know which way and how many times we encoded the password even if they know the salt value. We also give the possibility to store common passwords from different users with different encrypted values. This is due to the unique salts. 
<br> The control for when the account will be locked is done by the ``login()`` function. Specifically, it does not allow login after three attempts. While on each failure it updates the table with the counter increment and date.

<br> You can find the **python** code [here](https://github.com/Despoina2000/Register_Website/blob/main/site%20code/main.py).


<br> The **Flask** framework was used to run the site with the aid of python code. The libraries were downloaded with the commands:
```
pip3.7 install flask
pip3.7 install flask-sqlalchemy
pip3.7 install flask-login
```

<br> To run the [code](https://github.com/Despoina2000/Register_Website/blob/main/site%20code/main.py) I've made, you run the commands:
```
cd /var/www/html
python3.7 main.py
```
The result:
![image](https://github.com/Despoina2000/Register_Website/assets/66719546/009c28ed-de86-4ea0-82fe-c4fea0848081)


## Team Members
- [Despoina Papadopoulou](https://github.com/Despoina2000)





