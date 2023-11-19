let materialFirstCylinder, materialSecondCylinder, materialThirdCylinder, materialFourthCylinder;

const fullCircle = 2 * Math.PI;
const timing = 3;

// canvas conatiner
const container = document.getElementById("container");

// camera setup
const camera = new THREE.PerspectiveCamera(
	45,
	window.innerWidth / window.innerHeight,
	1,
	1000
);
camera.position.z = 350;
camera.position.y = 0;

// scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);

// light setup
const pointLight = new THREE.PointLight(0xffffff, 0);
pointLight.position.set(-200, 50, 100);
pointLight.castShadow = true;
scene.add(pointLight);

new TweenMax.to(pointLight, 1, {
	intensity: 2,
	delay: 1
})

// 3D models wrapper container
let cylinderContainer = new THREE.Object3D();

// 3D model geometry
const geometry = new THREE.CylinderBufferGeometry(150, 150, 50, 32, 1, true);

// object materials
materialFirstCylinder =  new THREE.MeshStandardMaterial({
	color: "#fff",
	transparent: true,
	side: THREE.DoubleSide,
	alphaTest: 0.5
});

materialSecondCylinder = new THREE.MeshStandardMaterial({
	color: "#fff",
	transparent: true,
	side: THREE.DoubleSide,
	alphaTest: 0.5
});

materialThirdCylinder = new THREE.MeshStandardMaterial({
	color: "#fff",
	transparent: true,
	side: THREE.DoubleSide,
	alphaTest: 0.5
});

materialFourthCylinder = new THREE.MeshStandardMaterial({
	color: "#fff",
	transparent: true,
	side: THREE.DoubleSide,
	alphaTest: 0.5
});


// text textures
let firstTex = document.createElement("canvas");
let firstContext = firstTex.getContext("2d");
let secondTex = document.createElement("canvas");
let secondContext = secondTex.getContext("2d");
let thirdTex = document.createElement("canvas");
let thirdContext = thirdTex.getContext("2d");
let fourthTex = document.createElement("canvas");
let fourthContext = fourthTex.getContext("2d");

firstTex.width = 
    secondTex.width = 
    thirdTex.width = 
    fourthTex.width = 4096;

firstTex.height = 
    secondTex.height = 
    thirdTex.height = 
    fourthTex.height = 256;

firstContext.font = 
    secondContext.font =
    thirdContext.font = 
    fourthContext.font = "Bold 300px Gill Sans";

firstContext.fillStyle = 
    secondContext.fillStyle = 
    thirdContext.fillStyle = 
    fourthContext.fillStyle = "white";

firstContext.fillText("инновации инновации инновации инновации", 0, 240, 4096);
secondContext.fillText(" Разум AGI разум LLM будущее ", 0, 240, 4096);
thirdContext.fillText("Технологии Умение Прогресс Генератив ", 0, 240, 4096);
fourthContext.fillText(" Бог Щанс Развитие Бог Попытка Начало ", 0, 240, 4096);

var firstTexture = new THREE.Texture(firstTex);
var secondTexture = new THREE.Texture(secondTex);
var thirdTexture = new THREE.Texture(thirdTex);
var fourthTexture = new THREE.Texture(fourthTex);

firstTexture.needsUpdate = 
	secondTexture.needsUpdate =
	thirdTexture.needsUpdate = 
	fourthTexture.needsUpdate = true;

materialFirstCylinder.alphaMap = firstTexture;
materialSecondCylinder.alphaMap = secondTexture;
materialThirdCylinder.alphaMap = thirdTexture;
materialFourthCylinder.alphaMap = fourthTexture;

materialFirstCylinder.alphaMap.magFilter = 
	materialSecondCylinder.alphaMap.magFilter = 
	materialThirdCylinder.alphaMap.magFilter = 
	materialFourthCylinder.alphaMap.magFilter = THREE.NearestFilter;

materialFirstCylinder.alphaMap.wrapT =
	materialSecondCylinder.alphaMap.wrapT = 
	materialThirdCylinder.alphaMap.wrapT = 
	materialFourthCylinder.alphaMap.wrapT = THREE.RepeatWrapping;

materialFirstCylinder.alphaMap.repeat.y = 
	materialSecondCylinder.alphaMap.repeat.y =
	materialThirdCylinder.alphaMap.repeat.y = 
	materialFourthCylinder.alphaMap.repeat.y = 1;

// init objects
cylinder1 = new THREE.Mesh(geometry, materialFirstCylinder);
cylinder2 = new THREE.Mesh(geometry, materialSecondCylinder);
cylinder3 = new THREE.Mesh(geometry, materialThirdCylinder);
cylinder4 = new THREE.Mesh(geometry, materialFourthCylinder);

// add objects to main object wrapper
cylinderContainer.add(cylinder1);
cylinderContainer.add(cylinder2);
cylinderContainer.add(cylinder3);
cylinderContainer.add(cylinder4);

// positioning objects
cylinder1.position.y = -75;
cylinder2.position.y = -25;
cylinder3.position.y = 25;
cylinder4.position.y = 75;

// positioning main object wrapper
cylinderContainer.position.z = -300;
cylinderContainer.position.x = 0;
cylinderContainer.rotation.x = - Math.PI / 4;
cylinderContainer.rotation.z = Math.PI / 6;

// adding main object wrapper to scene
scene.add(cylinderContainer);

// animations
const tweenPosetive = TweenMax.fromTo(
	[cylinder2.rotation, cylinder4.rotation],
	timing,
	{
		y: 0
	},
	{
		y: -fullCircle,
		repeat: -1,
		yoyo: true,
		ease: CustomEase.create(
			"custom",
			"M0,0,C0.406,0.114,0.4,0.888,0.558,1,0.701,1.101,0.906,1,1,1"
		)
	}
);

// animations (negative)
const tweenNegative = TweenMax.fromTo(
	[cylinder1.rotation, cylinder3.rotation],
	timing,
	{
		y: 0
	},
	{
		y: fullCircle,
		repeat: -1,
		yoyo: true,
		ease: CustomEase.create(
			"custom",
			"M0,0,C0.406,0.114,0.4,0.888,0.558,1,0.701,1.101,0.906,1,1,1"
		)
	}
);

// WebGL renderer
const renderer = new THREE.WebGLRenderer({
	antialias: true,
	alpha: true
});
renderer.setClearColor( 0x000000, 0 );
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);

// add canvas to dom
container.appendChild(renderer.domElement);

// 
window.addEventListener("resize", onWindowResize, false);

function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize(window.innerWidth, window.innerHeight);
}

function render() {
	renderer.render(scene, camera);
	requestAnimationFrame(render);
}

render();