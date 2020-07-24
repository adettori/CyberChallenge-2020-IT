<?php

class Post{
    private $title;
    private $body;

    public static function new_post($title, $body, $user_id){
        if(!Utils::validate(func_get_args())){
            return false;
        }
        $db = Db::get_db();
        // we don't want xss, at least we don't want easy xss :)
        $escaped_body = htmlspecialchars($body);
        $id = md5(openssl_random_pseudo_bytes(10));
        $q = 'INSERT INTO posts (id, title, body, user_id) VALUES ("%s","%s","%s","%s")';
        db::query($q,$id,$title,$escaped_body,$user_id);
        return self::from_id($id);
    }

    public static function delete($id){
        if(!Utils::validate(func_get_args())){
            return false;
        }

        //We need to ensure that the owner of the post is the same that is requesting its deletion
        $q = 'SELECT user_id FROM posts WHERE id = "%s"';
        $res = db::query($q, $id);
        
        // if the post doesn't exist
        if(!$res)
            return false;
        
        $owner_id = $res[0]['user_id'];
        if($owner_id === User::get_current_user()->getId()){
            db::query('DELETE FROM posts WHERE id = "%s"', $id);
            return true;
        }
        return false;
    }

    public static function format($str){
        if(!Utils::validate(func_get_args())){
            return false;
        }
        
        $str = preg_replace('#\[i\](.+?)\[/i\]#i','<span style="font-style:italic">$1</span>',$str);
        $str = preg_replace('#\[b\](.+?)\[/b\]#i','<strong>$1</strong>',$str);

        $str = nl2br($str);
        return $str;
    }

    public static function from_id($id){
        if(!Utils::validate(func_get_args())){
            return false;
        }
        
        $res = db::query('SELECT * FROM posts where id = "%s"', $id)[0];

        if(!$res){
            die('Post not found');
        }

        return new Post($res['id'], $res['title'], $res['body'], $res['user_id']);
    }

    public static function from_user(){
        $res = db::query('SELECT * FROM posts WHERE user_id = "%s"', $_SESSION['username']);
        $post_list=[];
    
        foreach($res as $data){
            $post_list[] = new Post($data['id'], $data['title'], $data['body'], $data['user_id']);
        }
        return $post_list;
    }

    private function __construct($id, $title, $body, $user_id){
        $this->id=$id;
        $this->title=$title;
        $this->body=$body;
        $this->user_id=$user_id;

    }

    public function getId(){
        return $this->id;
    }
    public function getTitle(){
        return $this->title;
    }
    public function getBody(){
        return self::format($this->body);
    }
}