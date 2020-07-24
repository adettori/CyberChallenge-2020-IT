<?php



/* init.sql */
/* 
CREATE TABLE users(
    fancy_username VARCHAR(255) NOT NULL,
    fancy_password VARCHAR(255) NOT NULL,
    PRIMARY KEY (fancy_username)
);


CREATE TABLE posts(
    id VARCHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    PRIMARY KEY( id),
    FOREIGN KEY (user_id) REFERENCES users(fancy_username)
);

INSERT INTO users(fancy_username,fancy_password) VALUES ('admin', '*REDACTED*');
INSERT INTO posts(id, title, body, user_id) VALUES ('*REDACTED*', 'wtf', 'why you are here', 'admin');
INSERT INTO posts(id, title, body, user_id) VALUES ('*REDACTED*', 'flag', 'congratz, CCIT{*REDACTED*}', 'admin');
*/
/**
 * Simple singleton for the db connection
 */
class Db{
    private static $db = false;

    public static function get_db(){
        if(!self::$db){
            try{
                $dsn = "sqlite:/srv/app.db";
                self::$db = new SQLite3('/srv/app.db');
                self::$db->enableExceptions(true);
            }catch(Exception $e){
                echo $e->getMessage();
                die("<br>\nCannot open the database. Please contact our majestic sysadmin:)");
            }
        }
        return self::$db;
    }

    public static function query(){
        $f_args = func_get_args();
        $query = $f_args[0];
        $args = array_slice($f_args, 1);

        $args_len = count($args);
        for($i = 0; $i<$args_len; $i++){
            $args[$i] = str_replace('"', '""', $args[$i]); 
        }
        $stm_query = vsprintf($query, $args);
        $db = self::get_db();
        $res = @$db->query($stm_query);
        if(!$res || $res->numColumns() === 0){
            return false;
        }
        // it seems that sqlite3 doesn't have a fetchAll wtf
        $fetch_array = [];
        while($c =  $res->fetchArray(SQLITE3_ASSOC)){
            $fetch_array[] = $c;
        }
        return $fetch_array;
    }
}