<?
$name = $_POST["name"];
echo "Привет ",$name," !";


$folderId = "b1ghoishr2f7ps5e0aom"; # Идентификатор каталога
$url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize";

$post = "text=" . urlencode($name) . "&lang=ru-RU&voice=filipp&folderId=${folderId}";
$headers = ['Authorization: Api-Key AQVNwdii6t7YAbHZXg826y_qIBKP90ogJgO_3qsN ' ];
$ch = curl_init();

curl_setopt($ch, CURLOPT_AUTOREFERER, TRUE);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
curl_setopt($ch, CURLOPT_HEADER, false);
if ($post !== false) {
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
}
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);


$response = curl_exec($ch);
if (curl_errno($ch)) {
    print "Error: " . curl_error($ch);
}
if (curl_getinfo($ch, CURLINFO_HTTP_CODE) != 200) {
    $decodedResponse = json_decode($response, true);
    echo "Error code: " . $decodedResponse["error_code"] . "\r\n";
    echo "Error message: " . $decodedResponse["error_message"] . "\r\n";
} else {
    file_put_contents("speech.ogg", $response);
}
curl_close($ch);

