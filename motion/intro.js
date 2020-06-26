var hth = window.innerHeight;
var wth = window.innerWidth;
var aspect = wth / hth

var grey = 0xf0f0f0;
var greyish = 0xcfcfcf;
var white = 0xffffff;
var camera, target, scene, light, renderer, controls,
      trans, orbit, cube, grid, loader, container, gcontrols;

var frustum = 150;

var c_left = 0.5 * frustum * aspect / - 2;
var c_right = 0.5 * frustum * aspect / 2;
var c_top = frustum / 2;
var c_bottom = frustum / - 2;
var c_near = 1
var c_far = 1000

import { STLLoader } from './lib/STLLoader.js';

var files = [
      'EVA_AX1-1.stl',
      'EVA_AX2-2.stl',
      'EVA_AX3-2.stl',
      'EVA_AX4-1.stl',
      'EVA_AX5-1.stl',
      'EVA_AX6-1.stl',
      'EVA_AX6_END-1.stl'
];

var theta_0, theta_1, theta_2, theta_3, theta_4, theta_5

init();
animate();


function init() {

      container = document.createElement('div');
      document.body.appendChild(container);

      scene = new THREE.Scene();
      scene.background = new THREE.Color(grey)
      scene.fog = new THREE.Fog(0x72645b, 2, 15);
      //camera = new THREE.OrthographicCamera(frustum * aspect / - 2, frustum * aspect / 2, frustum / 2, frustum / - 2, 1, 1000);
      camera = new THREE.PerspectiveCamera(30, aspect, 1, 3000)
      target = new THREE.Vector3(3, 0.15, 3)
      camera.position.set(4000, 6000, 8000);

      light = new THREE.AmbientLight(0xffffff, 0.475);
      grid = new THREE.GridHelper(250, 10);

      //light.position.set(0, 0, 1);
      renderer = new THREE.WebGLRenderer();
      renderer.setSize(wth, hth);
      container.appendChild(renderer.domElement);

      window.addEventListener('resize', () => {
            wth = window.innerWidth;
            hth = window.innerHeight;
            renderer.setSize(wth, hth);
            camera.aspect = wth / hth;
            camera.updateProjectionMatrix();
      });

      orbit = new THREE.OrbitControls(camera, renderer.domElement)
      orbit.dampingFactor = 0.05;
      orbit.screenSpacePanning = false;
      orbit.minDistance = 100;
      orbit.maxDistance = 3000;
      orbit.maxPolarAngle = Math.PI / 2;


      //orbit.addEventListener('change', render);
      trans = new THREE.TransformControls(camera, renderer.domElement)
      trans.addEventListener('change', render);

      trans.addEventListener('dragging-changed', (event) => {
            orbit.enabled = !event.value;

      });
      var geometry = new THREE.BoxGeometry(20, 20, 20);
      var material = new THREE.MeshNormalMaterial();
      //var material = new THREE.MeshLambertMaterial({ color: greyish, wireframe: false })

      cube = new THREE.Mesh(geometry, material)

      loader = new STLLoader();

      files.map(item => loader.load('./models/' + item, (geometry) => {
            var material = new THREE.MeshNormalMaterial();
            var mesh = new THREE.Mesh(geometry, material);
            // mesh.position.set(0, - 0.25, 0.6);
            // mesh.rotation.set(0, - Math.PI / 2, 0);
            // mesh.scale.set(0.5, 0.5, 0.5);
            mesh.castShadow = true;
            mesh.receiveShadow = true;
            scene.add(mesh);
      }))
      gcontrols = new function () {
            this.theta_0 = 0.00;
            this.theta_1 = 0.00;
            this.theta_2 = 0.00;
            this.theta_3 = 0.00;
            this.theta_4 = 0.00;
            this.theta_5 = 0.00;
            this.wireshow = false;
      }

      var gui = new dat.GUI();
      gui.add(gcontrols, 'theta_0', -1.5, 1.5);
      gui.add(gcontrols, 'theta_1', -1.5, 1.5);
      gui.add(gcontrols, 'theta_2', -1.5, 1.5);
      gui.add(gcontrols, 'theta_3', -1.5, 1.5);
      gui.add(gcontrols, 'theta_4', -1.5, 1.5);
      gui.add(gcontrols, 'theta_5', -1.5, 1.5);
      gui.add(gcontrols, 'wireshow');


      scene.add(light);
      scene.add(cube);
      scene.add(grid);
      scene.add(trans);
      trans.attach(cube);
}

function update() {
      theta_0 = gcontrols.theta_0;
      theta_1 = gcontrols.theta_1;
      theta_2 = gcontrols.theta_2;
      theta_3 = gcontrols.theta_3;
      theta_4 = gcontrols.theta_4;
      theta_5 = gcontrols.theta_5;
}

function render() {
      renderer.render(scene, camera);
      camera.lookAt(target);

}

function animate() {
      requestAnimationFrame(animate);
      orbit.update();
      update();
      render();
}

window.addEventListener('keydown', function (event) {
      switch (event.keyCode) {
            case 81: // Q
                  trans.setSpace(trans.space === "local" ? "world" : "local");
                  break;
            case 16: // shift
                  trans.setTranslationSnap(100);
                  trans.setRotationSnap(THREE.MathUtils.degToRad(15));
                  trans.setScaleSnap(0.25);
                  break;
            case 87: // W
                  trans.setMode("translate");
                  break;
            case 69: // E
                  trans.setMode("rotate");
                  break;
            case 82: // R
                  trans.setMode("scale");
                  break;
            case 187:
            case 107: // +, =, num+
                  trans.setSize(trans.size + 0.1);
                  break;
            case 189:
            case 109: // -, _, num-
                  trans.setSize(Math.max(trans.size - 0.1, 0.1));
                  break;
            case 88: // X
                  trans.showX = !trans.showX;
                  break;
            case 89: // Y
                  trans.showY = !trans.showY;
                  break;
            case 90: // Z
                  trans.showZ = !trans.showZ;
                  break;
            case 32: // Spacebar
                  trans.enabled = !trans.enabled;
                  break;
      }

});