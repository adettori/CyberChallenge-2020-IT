<?php

class User{
    private $username;

    public static function register($username, $password){
        if(!Utils::validate(func_get_args())){
            return false;
        }
        $q = 'INSERT INTO users(fancy_username, fancy_password) VALUES ("%s","%s")';
        try{
            $res = db::query($q, $username, $password);
        }catch(Exception $e){
            return false;
        }
        $_SESSION['username'] = $username;
        $_SESSION['csrf_token'] = self::gen_csrf_token();
        return new User($username);

    }

    public static function login($username, $password){
        if(!Utils::validate(func_get_args())){
            return false;
        }
        $q = 'SELECT fancy_username,fancy_password FROM users WHERE fancy_username = "%s" AND fancy_password = "%s"';
        $res = db::query($q, $username, $password);
        if($res && count($res)){
            $_SESSION['username'] = $res[0]['fancy_username'];
            $_SESSION['csrf_token'] = self::gen_csrf_token();
            return new User($res[0]['fancy_username']);
        }
        return false;
    }

    public static function get_current_user(){
        return self::is_logged();
    }

    public static function is_logged(){
        if(isset($_SESSION['username']))
            return new User($_SESSION['username']);
        else 
            return false;
    }
    /**
     * Some security functions
     */
    public static function get_csrf_token(){
        return $_SESSION['csrf_token'];
    }

    public static function gen_csrf_token(){
        return md5(openssl_random_pseudo_bytes(8));
    }
    
    public static function check_csrf_token($token){
        return $token === $_SESSION['csrf_token'];
    }

    private function __construct($username){
        $this->username = $username;
    }

    public function __toString(){
        return $this->username;
    }
    public function getId(){
        return $this->username;
    }
}