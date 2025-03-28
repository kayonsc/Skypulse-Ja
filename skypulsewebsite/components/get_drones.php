<?php
include "components/connect.php";
$result = $conn->query("SELECT * FROM drones");
$drones = [];
while ($row = $result->fetch_assoc()) {
    $drones[] = $row;
}
echo json_encode($drones);
?>