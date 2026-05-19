import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a2e);
scene.fog = new THREE.Fog(0x1a1a2e, 15, 25);

const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 50);
camera.position.set(7, 5, 7);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.5, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.maxPolarAngle = Math.PI / 2.2;
controls.minDistance = 3;
controls.maxDistance = 18;
controls.update();

const ambientLight = new THREE.AmbientLight(0x404060, 0.4);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffeedd, 1.2);
directionalLight.position.set(5, 10, 5);
directionalLight.castShadow = true;
directionalLight.shadow.mapSize.width = 1024;
directionalLight.shadow.mapSize.height = 1024;
directionalLight.shadow.camera.near = 0.1;
directionalLight.shadow.camera.far = 25;
directionalLight.shadow.camera.left = -12;
directionalLight.shadow.camera.right = 12;
directionalLight.shadow.camera.top = 12;
directionalLight.shadow.camera.bottom = -12;
scene.add(directionalLight);

const fillLight = new THREE.DirectionalLight(0x8888ff, 0.3);
fillLight.position.set(-4, 3, -4);
scene.add(fillLight);

const groundGeo = new THREE.PlaneGeometry(14, 14);
const groundMat = new THREE.MeshStandardMaterial({
  color: 0x2a2a3e,
  roughness: 0.9,
  metalness: 0.0,
});
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = 0;
ground.receiveShadow = true;
scene.add(ground);

const gridHelper = new THREE.GridHelper(14, 28, 0x555577, 0x3a3a55);
gridHelper.position.y = 0.01;
scene.add(gridHelper);

const COLORS = [
  0xff6b6b, 0x4ecdc4, 0x45b7d1, 0x96ceb4,
  0xffeaa7, 0xdda0dd, 0x98d8c8, 0xf7dc6f,
  0xbb8fce, 0x85c1e9, 0xf0b27a, 0x82e0aa,
];

function randomColor() {
  return COLORS[Math.floor(Math.random() * COLORS.length)];
}

const objects = [];
const GRAVITY = -22;
const GROUND_Y = 0;
const DAMPING = 0.35;
const FRICTION = 0.985;

let spawnType = 'cube';

function spawnObject(x, z) {
  const size = 0.3 + Math.random() * 0.25;
  let geo, halfSize;

  if (spawnType === 'cube') {
    geo = new THREE.BoxGeometry(size, size, size);
    halfSize = size / 2;
  } else {
    const radius = size * 0.55;
    geo = new THREE.SphereGeometry(radius, 10, 8);
    halfSize = radius;
  }

  const mat = new THREE.MeshStandardMaterial({
    color: randomColor(),
    roughness: 0.5,
    metalness: 0.05,
    flatShading: true,
  });

  const mesh = new THREE.Mesh(geo, mat);
  const spawnHeight = 2 + Math.random() * 2.5;
  mesh.position.set(x, spawnHeight, z);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  scene.add(mesh);

  objects.push({
    mesh,
    halfSize,
    velocity: new THREE.Vector3(
      (Math.random() - 0.5) * 0.6,
      -0.5 + Math.random() * 0.5,
      (Math.random() - 0.5) * 0.6,
    ),
    type: spawnType,
  });

  updateCount();
}

function clearAll() {
  for (const obj of objects) {
    scene.remove(obj.mesh);
    obj.mesh.geometry.dispose();
    obj.mesh.material.dispose();
  }
  objects.length = 0;
  updateCount();
}

function updateCount() {
  document.getElementById('count').textContent = objects.length;
}

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
const planeNormal = new THREE.Vector3(0, 1, 0);
const planePoint = new THREE.Vector3(0, 0, 0);
const groundPlane = new THREE.Plane().setFromNormalAndCoplanarPoint(planeNormal, planePoint);
const intersectionPoint = new THREE.Vector3();

renderer.domElement.addEventListener('click', (event) => {
  pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(pointer, camera);

  intersectionPoint.set(0, 0, 0);
  const hit = raycaster.ray.intersectPlane(groundPlane, intersectionPoint);

  if (hit) {
    const scatter = 0.15;
    spawnObject(
      intersectionPoint.x + (Math.random() - 0.5) * scatter,
      intersectionPoint.z + (Math.random() - 0.5) * scatter,
    );
  }
});

document.getElementById('btn-cube').addEventListener('click', () => {
  spawnType = 'cube';
  document.getElementById('btn-cube').classList.add('active');
  document.getElementById('btn-sphere').classList.remove('active');
});

document.getElementById('btn-sphere').addEventListener('click', () => {
  spawnType = 'sphere';
  document.getElementById('btn-sphere').classList.add('active');
  document.getElementById('btn-cube').classList.remove('active');
});

document.getElementById('btn-clear').addEventListener('click', clearAll);

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);

  const dt = Math.min(clock.getDelta(), 1 / 30);

  for (let i = 0; i < objects.length; i++) {
    const obj = objects[i];
    const vel = obj.velocity;
    const pos = obj.mesh.position;

    vel.y += GRAVITY * dt;

    pos.x += vel.x * dt;
    pos.y += vel.y * dt;
    pos.z += vel.z * dt;

    if (pos.y < GROUND_Y + obj.halfSize) {
      pos.y = GROUND_Y + obj.halfSize;

      if (Math.abs(vel.y) > 0.3) {
        vel.y *= -DAMPING;
      } else {
        vel.y = 0;
      }

      vel.x *= FRICTION;
      vel.z *= FRICTION;

      if (Math.abs(vel.x) < 0.001) vel.x = 0;
      if (Math.abs(vel.z) < 0.001) vel.z = 0;
    }

    if (obj.type === 'cube') {
      obj.mesh.rotation.x += vel.z * dt * 3;
      obj.mesh.rotation.z -= vel.x * dt * 3;
    }
  }

  controls.update();
  renderer.render(scene, camera);
}

animate();

spawnObject(0, 0);
spawnObject(1.2, 0.8);
spawnObject(-1, -0.7);
spawnObject(0.5, -1.3);
spawnObject(-1.1, 0.9);
spawnObject(0.3, -0.3);
