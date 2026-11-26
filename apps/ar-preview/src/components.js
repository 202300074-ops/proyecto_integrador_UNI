const AFRAME = window.AFRAME;
const THREE = AFRAME.THREE;

function seededRandom(seed) {
  let value = seed;
  return () => {
    value |= 0;
    value = (value + 0x6d2b79f5) | 0;
    let t = Math.imul(value ^ (value >>> 15), 1 | value);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

AFRAME.registerComponent('bee-wander', {
  schema: {
    center: { type: 'vec3', default: { x: 0, y: 1.1, z: -2.7 } },
    radiusX: { type: 'number', default: 0.8 },
    radiusZ: { type: 'number', default: 0.5 },
    height: { type: 'number', default: 0.2 },
    speed: { type: 'number', default: 0.5 },
    phase: { type: 'number', default: 0 },
    yawOffset: { type: 'number', default: 0 },
    bank: { type: 'number', default: 0.12 }
  },

  init() {
    this.time = this.data.phase;
    this.current = new THREE.Vector3();
    this.previous = new THREE.Vector3();
    this.sample(0, this.current);
    this.previous.copy(this.current);
    this.el.object3D.position.copy(this.current);
  },

  sample(time, target) {
    const { center, radiusX, radiusZ, height, phase } = this.data;
    const angle = time + phase;
    target.set(
      center.x + Math.sin(angle * 1.15) * radiusX + Math.sin(angle * 0.47 + 1.3) * radiusX * 0.18,
      center.y + Math.sin(angle * 1.9 + 0.8) * height + Math.sin(angle * 3.2) * 0.03,
      center.z + Math.cos(angle * 0.93 + 0.4) * radiusZ + Math.cos(angle * 0.37 + 2.2) * radiusZ * 0.16
    );
    return target;
  },

  tick(time, delta) {
    const step = Math.min(delta / 1000, 0.05);
    this.time += step * this.data.speed;
    this.sample(this.time, this.current);

    const dx = this.current.x - this.previous.x;
    const dz = this.current.z - this.previous.z;
    if (Math.abs(dx) + Math.abs(dz) > 0.000001) {
      const targetYaw = Math.atan2(-dx, -dz) + this.data.yawOffset;
      const currentYaw = this.el.object3D.rotation.y;
      const difference = Math.atan2(
        Math.sin(targetYaw - currentYaw),
        Math.cos(targetYaw - currentYaw)
      );
      this.el.object3D.rotation.y = currentYaw + difference * Math.min(1, step * 6);
    }

    this.el.object3D.rotation.z = Math.sin(this.time * 2.1) * this.data.bank;
    this.el.object3D.position.copy(this.current);
    this.previous.copy(this.current);
  }
});

AFRAME.registerComponent('flower', {
  schema: {
    stem: { type: 'color', default: '#3f6b2f' },
    petals: { type: 'color', default: '#f4e6a4' },
    center: { type: 'color', default: '#d18a2f' },
    height: { type: 'number', default: 0.38 },
    size: { type: 'number', default: 1 },
    sway: { type: 'number', default: 0.06 }
  },

  init() {
    const { stem, petals, center, height, size } = this.data;
    const stemElement = document.createElement('a-cylinder');
    stemElement.setAttribute('radius', 0.012 * size);
    stemElement.setAttribute('height', height);
    stemElement.setAttribute('position', `0 ${height / 2} 0`);
    stemElement.setAttribute('segments-radial', 6);
    stemElement.setAttribute('material', `color: ${stem}; roughness: 1; flatShading: true`);
    this.el.appendChild(stemElement);

    for (const side of [-1, 1]) {
      const leaf = document.createElement('a-sphere');
      leaf.setAttribute('position', `${side * 0.055 * size} ${height * 0.42} ${0.01 * size}`);
      leaf.setAttribute('rotation', `0 0 ${side * 35}`);
      leaf.setAttribute('scale', `${0.095 * size} ${0.018 * size} ${0.045 * size}`);
      leaf.setAttribute('segments-width', 6);
      leaf.setAttribute('segments-height', 4);
      leaf.setAttribute('material', `color: ${stem}; roughness: 1; flatShading: true`);
      this.el.appendChild(leaf);
    }

    this.head = document.createElement('a-entity');
    this.head.setAttribute('position', `0 ${height} 0`);
    this.el.appendChild(this.head);

    const petalCount = 6;
    for (let index = 0; index < petalCount; index += 1) {
      const angle = (index / petalCount) * Math.PI * 2;
      const petal = document.createElement('a-sphere');
      petal.setAttribute('position', `${Math.cos(angle) * 0.075 * size} 0 ${Math.sin(angle) * 0.075 * size}`);
      petal.setAttribute('rotation', `0 ${(-angle * 180) / Math.PI} 0`);
      petal.setAttribute('scale', `${0.085 * size} ${0.02 * size} ${0.05 * size}`);
      petal.setAttribute('segments-width', 8);
      petal.setAttribute('segments-height', 5);
      petal.setAttribute('material', `color: ${petals}; roughness: 0.85; flatShading: true`);
      this.head.appendChild(petal);
    }

    const centerElement = document.createElement('a-sphere');
    centerElement.setAttribute('radius', 0.036 * size);
    centerElement.setAttribute('scale', '1 0.55 1');
    centerElement.setAttribute('segments-width', 8);
    centerElement.setAttribute('segments-height', 5);
    centerElement.setAttribute('material', `color: ${center}; roughness: 0.9; flatShading: true`);
    this.head.appendChild(centerElement);

    this.phase = Math.random() * Math.PI * 2;
  },

  tick(time) {
    this.head.object3D.rotation.z = Math.sin(time / 1400 + this.phase) * this.data.sway;
    this.head.object3D.rotation.x = Math.cos(time / 1800 + this.phase) * this.data.sway * 0.6;
  }
});

AFRAME.registerComponent('grass-clump', {
  schema: {
    count: { type: 'int', default: 7 },
    radius: { type: 'number', default: 0.18 },
    color: { type: 'color', default: '#6f8f48' }
  },

  init() {
    const random = seededRandom(Math.floor(Math.random() * 1000000));
    const randomColor = new THREE.Color(this.data.color);

    for (let index = 0; index < this.data.count; index += 1) {
      const blade = document.createElement('a-cone');
      const angle = random() * Math.PI * 2;
      const distance = random() * this.data.radius;
      const height = 0.15 + random() * 0.22;
      const tint = randomColor.clone().offsetHSL(0, 0, (random() - 0.5) * 0.08);

      blade.setAttribute('position', `${Math.cos(angle) * distance} ${height / 2} ${Math.sin(angle) * distance}`);
      blade.setAttribute('rotation', `${(random() - 0.5) * 16} ${random() * 360} ${(random() - 0.5) * 22}`);
      blade.setAttribute('radius-bottom', 0.018 + random() * 0.012);
      blade.setAttribute('radius-top', 0.002);
      blade.setAttribute('height', height);
      blade.setAttribute('segments-radial', 4);
      blade.setAttribute('material', `color: #${tint.getHexString()}; roughness: 1; flatShading: true`);
      this.el.appendChild(blade);
    }
  }
});

AFRAME.registerComponent('foliage-sway', {
  schema: {
    amount: { type: 'number', default: 0.02 },
    speed: { type: 'number', default: 0.0012 }
  },

  init() {
    this.phase = Math.random() * Math.PI * 2;
    this.baseRotation = this.el.object3D.rotation.clone();
  },

  tick(time) {
    this.el.object3D.rotation.z = this.baseRotation.z + Math.sin(time * this.data.speed + this.phase) * this.data.amount;
    this.el.object3D.rotation.x = this.baseRotation.x + Math.cos(time * this.data.speed * 0.8 + this.phase) * this.data.amount * 0.5;
  }
});

AFRAME.registerComponent('farm-tree', {
  schema: {
    height: { type: 'number', default: 3.8 },
    crownRadius: { type: 'number', default: 1.15 },
    trunkColor: { type: 'color', default: '#68472f' },
    leafColor: { type: 'color', default: '#527c40' },
    variant: { type: 'int', default: 0 }
  },

  init() {
    const { height, crownRadius, trunkColor, leafColor, variant } = this.data;
    const trunk = document.createElement('a-cylinder');
    trunk.setAttribute('position', `0 ${height / 2} 0`);
    trunk.setAttribute('radius', Math.max(0.16, height * 0.055));
    trunk.setAttribute('height', height);
    trunk.setAttribute('segments-radial', 7);
    trunk.setAttribute('material', `color: ${trunkColor}; roughness: 1; flatShading: true`);
    this.el.appendChild(trunk);

    for (const [index, branchData] of [
      [-0.42, height * 0.68, -18],
      [0.46, height * 0.76, 22]
    ].entries()) {
      const [offset, y, angle] = branchData;
      const branch = document.createElement('a-cylinder');
      branch.setAttribute('position', `${offset} ${y} 0`);
      branch.setAttribute('rotation', `0 0 ${angle}`);
      branch.setAttribute('radius', Math.max(0.07, height * 0.025));
      branch.setAttribute('height', height * (index === 0 ? 0.44 : 0.4));
      branch.setAttribute('segments-radial', 6);
      branch.setAttribute('material', `color: ${trunkColor}; roughness: 1; flatShading: true`);
      this.el.appendChild(branch);
    }

    const crownOffsets = [
      [0, height * 0.96, 0, 1],
      [-0.7, height * 0.82, 0.12, 0.72],
      [0.68, height * 0.86, -0.08, 0.76],
      [0.08, height * 1.28, 0.14, 0.68]
    ];
    for (const [index, [x, y, z, scale]] of crownOffsets.entries()) {
      const crown = document.createElement('a-icosahedron');
      const color = new THREE.Color(leafColor).offsetHSL(0, 0, (index - 1.5) * 0.018 + variant * 0.008);
      crown.setAttribute('position', `${x * crownRadius} ${y} ${z * crownRadius}`);
      crown.setAttribute('radius', crownRadius * scale);
      crown.setAttribute('detail', '1');
      crown.setAttribute('material', `color: #${color.getHexString()}; roughness: 1; flatShading: true`);
      crown.setAttribute('foliage-sway', `amount: 0.018; speed: ${0.0008 + index * 0.00012}`);
      this.el.appendChild(crown);
    }
  }
});

AFRAME.registerComponent('pond-fish', {
  schema: {
    center: { type: 'vec3', default: { x: 8, y: 0.2, z: -18 } },
    radiusX: { type: 'number', default: 1.2 },
    radiusZ: { type: 'number', default: 0.8 },
    speed: { type: 'number', default: 0.35 },
    phase: { type: 'number', default: 0 }
  },

  tick(time) {
    const angle = time * 0.001 * this.data.speed + this.data.phase;
    const nextX = this.data.center.x + Math.cos(angle) * this.data.radiusX;
    const nextZ = this.data.center.z + Math.sin(angle) * this.data.radiusZ;
    const dx = nextX - this.el.object3D.position.x;
    const dz = nextZ - this.el.object3D.position.z;
    this.el.object3D.position.set(nextX, this.data.center.y + Math.sin(angle * 2) * 0.012, nextZ);
    this.el.object3D.rotation.y = Math.atan2(-dx, -dz);
  }
});

AFRAME.registerComponent('wing-flap', {
  schema: {
    amount: { type: 'number', default: 0.7 },
    frequency: { type: 'number', default: 8 },
    phase: { type: 'number', default: 0 },
    side: { type: 'int', default: 1 }
  },

  init() {
    this.baseRotation = this.el.object3D.rotation.clone();
  },

  tick(time) {
    const angle = (time / 1000) * this.data.frequency * Math.PI * 2 + this.data.phase;
    this.el.object3D.rotation.z =
      this.baseRotation.z + Math.sin(angle) * this.data.amount * this.data.side;
  }
});

AFRAME.registerComponent('ambient-bee', {
  init() {
    const body = document.createElement('a-sphere');
    body.setAttribute('position', '0 0 0.015');
    body.setAttribute('radius', '0.082');
    body.setAttribute('scale', '0.78 0.72 1.35');
    body.setAttribute('material', 'color: #d99c32; roughness: 0.86; flatShading: true');
    this.el.appendChild(body);

    for (const z of [-0.02, 0.055]) {
      const stripe = document.createElement('a-sphere');
      stripe.setAttribute('position', `0 0 ${z}`);
      stripe.setAttribute('radius', '0.074');
      stripe.setAttribute('scale', '0.82 0.86 0.22');
      stripe.setAttribute('material', 'color: #342b20; roughness: 1; flatShading: true');
      this.el.appendChild(stripe);
    }

    const head = document.createElement('a-sphere');
    head.setAttribute('position', '0 0.005 -0.105');
    head.setAttribute('radius', '0.052');
    head.setAttribute('material', 'color: #29251f; roughness: 0.9; flatShading: true');
    this.el.appendChild(head);

    for (const side of [-1, 1]) {
      const wing = document.createElement('a-entity');
      wing.setAttribute('position', `${side * 0.035} 0.055 0.005`);
      wing.setAttribute('wing-flap', `amount: 0.65; frequency: 12; phase: ${side < 0 ? 1.4 : 0}; side: ${side}`);
      const membrane = document.createElement('a-plane');
      membrane.setAttribute('position', `${side * 0.075} 0 0`);
      membrane.setAttribute('rotation', '0 0 0');
      membrane.setAttribute('width', '0.14');
      membrane.setAttribute('height', '0.075');
      membrane.setAttribute('material', 'color: #fff2d5; opacity: 0.78; transparent: true; side: double');
      wing.appendChild(membrane);
      this.el.appendChild(wing);
    }
  }
});
