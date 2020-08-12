function findInitialVelocity(initialPosition, targetPosition, timeofFlight) {

  var dx = targetPosition.x - initialPosition.x;
  var dy = targetPosition.y - initialPosition.y;
  var dz = targetPosition.z - initialPosition.z;

  console.log(GRAVITY);


  var v_x = dx / timeofFlight;
  var v_y = (dy / timeofFlight) - (0.5 * GRAVITY * timeofFlight);
  var v_z = dz / timeofFlight;

  console.log(v_x);
  return new THREE.Vector3(v_x, v_y, v_z);



}
