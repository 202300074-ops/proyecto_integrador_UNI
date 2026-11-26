import assert from 'node:assert/strict';
import { canOccupy, FARM_NAVIGATION, normalizeInput, resolvePosition } from '../src/vr-navigation.js';

const world = {
  centerX: 0,
  centerZ: -4,
  radius: 38,
  playerRadius: 0.45,
  obstacles: [
    { x: 1.6, z: -5.1, radius: 0.7 },
    { x: 8, z: -18, radius: 5 }
  ]
};

assert.equal(canOccupy(0, 0, world), true, 'should allow the open starting clearing');
assert.equal(canOccupy(40, -4, world), false, 'should block movement outside the farm boundary');
assert.equal(canOccupy(1.7, -5, world), false, 'should block walking into a tree trunk');
assert.equal(canOccupy(8, -18, world), false, 'should block entering the pond');
assert.deepEqual(
  resolvePosition({ x: 0, z: 0 }, { x: 1.7, z: -5 }, world),
  { x: 0, z: 0 },
  'should keep the previous safe position when the next step collides'
);
assert.deepEqual(
  resolvePosition({ x: 0, z: 0 }, { x: -4, z: 2 }, world),
  { x: -4, z: 2 },
  'should allow a clear path toward the garden behind the visitor'
);

for (const [zone, x, z] of [
  ['inicio', 0, 0],
  ['jardin', 1.45, -1.55],
  ['jobon', -2.4, -2.1],
  ['palapa', -8.6, -1.6],
  ['lago', 6.5, -12.5]
]) {
  assert.equal(canOccupy(x, z, FARM_NAVIGATION), true, `teleport ${zone} debe caer en suelo libre`);
}

assert.equal(canOccupy(8, -18, FARM_NAVIGATION), false, 'el lago real debe seguir bloqueando el paso');
assert.equal(canOccupy(0, -48, FARM_NAVIGATION), false, 'el límite real de la granja debe contener al visitante');

const diagonal = normalizeInput(1, 1);
assert.ok(Math.abs(diagonal.magnitude - 1) < 1e-9, 'la diagonal debe limitarse a velocidad máxima');
assert.ok(Math.abs(diagonal.forward - Math.SQRT1_2) < 1e-9, 'la diagonal debe repartirse en ambos ejes');
assert.ok(Math.abs(diagonal.strafe - Math.SQRT1_2) < 1e-9, 'la diagonal debe repartirse en ambos ejes');

const analog = normalizeInput(0.5, 0);
assert.ok(Math.abs(analog.forward - 0.5) < 1e-9, 'el joystick debe conservar la intensidad parcial');
assert.deepEqual(normalizeInput(0, 0), { forward: 0, strafe: 0, magnitude: 0 }, 'sin entrada no debe moverse');

console.log('VR_NAVIGATION_OK: bounds, tree/pond collisions and clear farm path.');