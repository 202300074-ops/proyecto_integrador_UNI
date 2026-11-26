export const FARM_NAVIGATION = Object.freeze({
  centerX: 0,
  centerZ: -5,
  radius: 42,
  playerRadius: 0.45,
  obstacles: Object.freeze([
    Object.freeze({ x: -0.7, z: -3.3, radius: 1.0 }),
    Object.freeze({ x: 1.6, z: -5.1, radius: 0.72 }),
    Object.freeze({ x: -8, z: -3, radius: 0.65 }),
    Object.freeze({ x: -11, z: -4, radius: 0.65 }),
    Object.freeze({ x: 8, z: -7, radius: 0.65 }),
    Object.freeze({ x: 2, z: 11, radius: 0.65 }),
    Object.freeze({ x: -9, z: -8, radius: 0.75 }),
    Object.freeze({ x: 9, z: -11, radius: 0.75 }),
    Object.freeze({ x: -16, z: -2, radius: 0.75 }),
    Object.freeze({ x: 16, z: -5, radius: 0.75 }),
    Object.freeze({ x: -10, z: 8, radius: 0.75 }),
    Object.freeze({ x: 11, z: 9, radius: 0.75 }),
    Object.freeze({ x: -5, z: 18, radius: 0.75 }),
    Object.freeze({ x: 8, z: 20, radius: 0.75 }),
    Object.freeze({ x: -21, z: 4, radius: 0.75 }),
    Object.freeze({ x: 22, z: 3, radius: 0.75 }),
    Object.freeze({ x: -18, z: 21, radius: 0.75 }),
    Object.freeze({ x: 18, z: 22, radius: 0.75 }),
    Object.freeze({ x: -10, z: -7, radius: 1.8 }),
    Object.freeze({ x: 8, z: -18, radius: 5.0 })
  ])
});

export function canOccupy(x, z, world = FARM_NAVIGATION) {
  const { centerX, centerZ, radius, playerRadius, obstacles = [] } = world;
  const values = [x, z, centerX, centerZ, radius, playerRadius];
  if (!values.every(Number.isFinite) || radius <= playerRadius || playerRadius < 0) return false;

  const distanceFromCenter = Math.hypot(x - centerX, z - centerZ);
  if (distanceFromCenter + playerRadius > radius) return false;

  return obstacles.every((obstacle) => {
    if (![obstacle.x, obstacle.z, obstacle.radius].every(Number.isFinite) || obstacle.radius < 0) {
      return false;
    }
    return Math.hypot(x - obstacle.x, z - obstacle.z) >= obstacle.radius + playerRadius;
  });
}

export function resolvePosition(current, candidate, world = FARM_NAVIGATION) {
  if (canOccupy(candidate.x, candidate.z, world)) {
    return { x: candidate.x, z: candidate.z };
  }
  return { x: current.x, z: current.z };
}

export function normalizeInput(forward, strafe) {
  const magnitude = Math.hypot(forward, strafe);
  if (!Number.isFinite(magnitude) || magnitude < 0.0001) {
    return { forward: 0, strafe: 0, magnitude: 0 };
  }
  const scale = Math.min(1, magnitude) / magnitude;
  return {
    forward: forward * scale,
    strafe: strafe * scale,
    magnitude: Math.min(1, magnitude)
  };
}
