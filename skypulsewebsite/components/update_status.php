<?php
include("connect.php");  // Include database connection

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $tracking_id = $_POST["tracking_id"];
    $new_status = $_POST["new_status"];

    $query = "UPDATE tracking SET current_status='$new_status', last_updated=NOW() WHERE tracking_id='$tracking_id'";
    
    if (mysqli_query($conn, $query)) {
        echo json_encode(["success" => "Status updated successfully"]);
    } else {
        echo json_encode(["error" => "Failed to update status"]);
    }
}

mysqli_close($conn);
?>