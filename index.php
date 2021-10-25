
<?php
if ($argv[1]) {
    $category = $argv[1];
} else {
    $category = "international";
}

$url = "https://www.news24.jp/" . $category . "/index.jsonp";

function get_JSONP($url)
{
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => '',
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 0,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => 'GET',
    ));
    $output = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
   if($http_code === 200) return $output;
   if($http_code !== 200) {
       echo "nonexistent category" . PHP_EOL; 
       return null;
   }
}

function jsonp_decode($jsonp)
{
    if ($jsonp[0] !== '[' && $jsonp[0] !== '{') {
        $jsonp = substr($jsonp, strpos($jsonp, '('));
    }
    $jsonp = trim($jsonp);
    $jsonp = trim($jsonp, "(");
    $jsonp = str_replace(");", "", $jsonp);
    // var_dump($jsonp);
    $json_arr = json_decode($jsonp, true);

    switch (json_last_error()) {
        case JSON_ERROR_NONE:
            print ' - Ошибок нет' . PHP_EOL;
            break;
        case JSON_ERROR_DEPTH:
            echo ' - Достигнута максимальная глубина стека' . PHP_EOL;
            break;
        case JSON_ERROR_STATE_MISMATCH:
            echo ' - Некорректные разряды или несоответствие режимов' . PHP_EOL;
            break;
        case JSON_ERROR_CTRL_CHAR:
            echo ' - Некорректный управляющий символ' . PHP_EOL;
            break;
        case JSON_ERROR_SYNTAX:
            echo ' - Синтаксическая ошибка, некорректный JSON' . PHP_EOL;
            break;
        case JSON_ERROR_UTF8:
            echo ' - Некорректные символы UTF-8, возможно неверно закодирован' .  PHP_EOL;
            break;
        default:
            echo ' - Неизвестная ошибка' .  PHP_EOL;
            break;
    }
    $json_arr = $json_arr["articleList"];
    //print_r($json_arr) ; // ["categoryName"]
    echo "category:" . $json_arr[0]["categoryKeyword"] . PHP_EOL;
    for ($j = 0; $j < count($json_arr); $j++) {
        echo $j + 1 . ") " . $json_arr[$j]["newsHeadLine"] .  PHP_EOL;
    }
}

$jsonp = get_JSONP($url);
if($jsonp !== null) jsonp_decode($jsonp);


