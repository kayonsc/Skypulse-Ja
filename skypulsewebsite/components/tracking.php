<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

include("connect.php");  // Database connection

if(isset($_GET['tracking_id'])) {
    $tracking_id = $_GET['tracking_id'];
    
    $query = "SELECT customer_name, current_status, last_updated FROM tracking WHERE tracking_id='$tracking_id'";
    $result = mysqli_query($conn, $query);
    
    if(mysqli_num_rows($result) > 0) {
        $row = mysqli_fetch_assoc($result);
        echo json_encode($row);
    } else {
        echo json_encode(["error" => "Tracking ID not found"]);
    }
} else {
    echo json_encode(["error" => "Invalid request"]);
}

mysqli_close($conn);
?>
