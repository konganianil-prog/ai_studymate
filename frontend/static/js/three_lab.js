/**
 * AI STUDY MATE - 3D Interactive Educational Learning Lab
 * Powered by Three.js & OrbitControls
 */

class Interactive3DLab {
  constructor(canvasContainerId) {
    this.container = document.getElementById(canvasContainerId);
    if (!this.container) return;

    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.controls = null;
    this.currentModelGroup = null;
    this.animationFrameId = null;
    this.isAutoRotating = true;
    this.isWireframe = false;
    this.clock = new THREE.Clock();
    this.currentTopicKey = 'atom';

    // Model Registry
    this.registry = {
      'atom': {
        name: 'Atomic Structure & Bohr Model',
        category: 'Physics & Chemistry',
        description: 'The Bohr model of the atom depicts a dense central nucleus composed of protons and neutrons, orbited by quantized electron shells. Electrons maintain stable orbits without radiating energy except when transitioning between discrete energy levels.',
        parts: [
          { name: 'Nucleus', desc: 'Dense core containing positively charged protons and neutral neutrons.' },
          { name: 'Inner Shell (K-shell)', desc: 'Lowest energy level, holding up to 2 quantum-bound electrons.' },
          { name: 'Outer Shell (L-shell)', desc: 'Higher energy orbital path with valence electrons.' },
          { name: 'Electrons', desc: 'Subatomic particles with negative charge exhibiting wave-particle duality.' }
        ],
        builder: this.buildAtomModel.bind(this)
      },
      'dna': {
        name: 'DNA Double Helix Structure',
        category: 'Biology & Genetics',
        description: 'Deoxyribonucleic acid (DNA) is a double-stranded antiparallel polymer composed of repeating nucleotides. Complementary nitrogenous bases (Adenine-Thymine, Guanine-Cytosine) form hydrogen bonds that stabilize the double helix.',
        parts: [
          { name: 'Sugar-Phosphate Backbone', desc: 'Alternating deoxyribose and phosphate groups running in 5\' to 3\' directions.' },
          { name: 'Base Pairs (Rungs)', desc: 'A-T pairs (2 hydrogen bonds) and G-C pairs (3 hydrogen bonds).' },
          { name: 'Major & Minor Grooves', desc: 'Helical indentations that allow regulatory proteins to bind.' }
        ],
        builder: this.buildDNAModel.bind(this)
      },
      'heart': {
        name: 'Human Heart Anatomy',
        category: 'Human Biology & Anatomy',
        description: 'A muscular organ composed of four chambers (two atria, two ventricles) responsible for pumping oxygenated and deoxygenated blood through systemic and pulmonary circulatory circuits.',
        parts: [
          { name: 'Left Ventricle', desc: 'Thick muscular chamber pumping oxygenated blood into the aorta.' },
          { name: 'Right Ventricle', desc: 'Pumps deoxygenated blood to the lungs for gas exchange.' },
          { name: 'Aorta & Pulmonary Artery', desc: 'Primary arterial vessels distributing high-pressure blood flow.' },
          { name: 'Atria', desc: 'Receiving chambers for venous blood return.' }
        ],
        builder: this.buildHeartModel.bind(this)
      },
      'brain': {
        name: 'Human Brain Hemispheres',
        category: 'Neuroscience & Cognition',
        description: 'The central organ of the nervous system consisting of the cerebrum (divided into left and right hemispheres connected by the corpus callosum), cerebellum, and brainstem.',
        parts: [
          { name: 'Left Hemisphere', desc: 'Associated with analytical reasoning, language, and logic.' },
          { name: 'Right Hemisphere', desc: 'Associated with spatial orientation, creativity, and pattern recognition.' },
          { name: 'Cerebellum', desc: 'Coordinates voluntary motor movements, posture, and balance.' },
          { name: 'Neural Impulses', desc: 'Electrical and chemical synapses communicating via neurotransmitters.' }
        ],
        builder: this.buildBrainModel.bind(this)
      },
      'solar_system': {
        name: 'Solar System & Planetary Orbits',
        category: 'Astrophysics & Astronomy',
        description: 'Gravitationally bound system comprising the Sun and objects orbiting it, including the eight major planets, asteroids, and orbital satellites obeying Keplerian laws of planetary motion.',
        parts: [
          { name: 'The Sun', desc: 'G-type main-sequence star generating energy through thermonuclear fusion.' },
          { name: 'Inner Terrestrial Planets', desc: 'Mercury, Venus, Earth, and Mars composed primarily of silicate rock and metals.' },
          { name: 'Gas Giants', desc: 'Jupiter and Saturn with prominent ring systems and massive magnetic fields.' },
          { name: 'Orbital Planes', desc: 'Elliptical trajectories dictated by Newtonian gravitational mechanics.' }
        ],
        builder: this.buildSolarSystemModel.bind(this)
      },
      'cpu': {
        name: 'Microprocessor (CPU) Architecture',
        category: 'Computer Systems Architecture',
        description: 'The primary logic engine of a computer system containing arithmetic logic units (ALU), control units, hardware register files, cache hierarchies, and interconnect buses on a silicon die.',
        parts: [
          { name: 'Silicon Die & Cores', desc: 'Multi-core processing units executing instructions in parallel.' },
          { name: 'L1/L2/L3 Cache Buffer', desc: 'Ultra-fast SRAM memory layers reducing memory access latency.' },
          { name: 'Integrated Heat Spreader', desc: 'Thermal dissipation metal plate protecting microscopic transistors.' },
          { name: 'LGA / BGA Contact Pins', desc: 'Gold-plated pin grid array transmitting clock and data signals to the motherboard.' }
        ],
        builder: this.buildCPUModel.bind(this)
      },
      'network': {
        name: 'Computer Network Star Topology',
        category: 'Computer Networking',
        description: 'A network configuration where all host nodes are individually connected to a central network hub or switch. Eliminates single point failure in node cabling and simplifies packet diagnosis.',
        parts: [
          { name: 'Central Switch', desc: 'Intelligent Layer-2/Layer-3 multiport bridge forwarding frame packets by MAC/IP.' },
          { name: 'Workstations / Host Nodes', desc: 'Client computers issuing network requests.' },
          { name: 'Server Rack', desc: 'High-availability repository serving databases and application services.' },
          { name: 'Transmission Cables', desc: 'Twisted-pair Ethernet cables maintaining full-duplex gigabit bandwidth.' }
        ],
        builder: this.buildNetworkModel.bind(this)
      },
      'blockchain': {
        name: 'Blockchain Distributed Ledger',
        category: 'Distributed Systems & Cryptography',
        description: 'A decentralized, immutable chronological chain of cryptographic blocks. Each block contains transactions, a proof-of-work nonce, and a SHA-256 hash pointer to the preceding block.',
        parts: [
          { name: 'Block Header', desc: 'Metadata containing version, timestamp, and target difficulty.' },
          { name: 'Merkle Tree Transactions', desc: 'Binary tree of cryptographic transaction hashes.' },
          { name: 'Cryptographic Hash Link', desc: 'Pointer to previous block ensuring immutability across peer nodes.' },
          { name: 'Distributed Consensus', desc: 'Peer verification protocols (PoW / PoS) validating state updates.' }
        ],
        builder: this.buildBlockchainModel.bind(this)
      }
    };

    this.initThree();
    this.setupUIEvents();
    this.loadModel('atom');
  }

  initThree() {
    // 1. Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0c1022);

    // 2. Camera
    const aspect = this.container.clientWidth / this.container.clientHeight;
    this.camera = new THREE.PerspectiveCamera(45, aspect, 0.1, 1000);
    this.camera.position.set(0, 5, 14);

    // 3. Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    this.container.appendChild(this.renderer.domElement);

    // 4. OrbitControls
    if (typeof THREE.OrbitControls !== 'undefined') {
      this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.05;
      this.controls.maxDistance = 40;
      this.controls.minDistance = 2;
    }

    // 5. Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    this.scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0x6c63ff, 1.2);
    dirLight1.position.set(10, 20, 15);
    this.scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x00c9a7, 0.8);
    dirLight2.position.set(-10, -10, -10);
    this.scene.add(dirLight2);

    const pointLight = new THREE.PointLight(0xffffff, 1, 50);
    pointLight.position.set(0, 0, 0);
    this.scene.add(pointLight);

    // 6. Grid helper for spatial reference
    const gridHelper = new THREE.GridHelper(30, 30, 0x1b2340, 0x151b33);
    gridHelper.position.y = -4;
    this.scene.add(gridHelper);

    // 7. Window resize handler
    window.addEventListener('resize', this.onWindowResize.bind(this));

    // 8. Start Animation Loop
    this.animate();
  }

  onWindowResize() {
    if (!this.container || !this.camera || !this.renderer) return;
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  animate() {
    this.animationFrameId = requestAnimationFrame(this.animate.bind(this));

    const delta = this.clock.getDelta();
    const elapsedTime = this.clock.getElapsedTime();

    if (this.controls) {
      this.controls.update();
    }

    // Model specific procedural animations
    if (this.currentModelGroup) {
      if (this.isAutoRotating) {
        this.currentModelGroup.rotation.y += 0.006;
      }

      // Special animations for specific models
      if (this.currentTopicKey === 'atom') {
        const electrons = this.currentModelGroup.userData.electrons;
        if (electrons) {
          electrons.forEach((el, idx) => {
            const speed = 1.8 + idx * 0.4;
            const angle = elapsedTime * speed + idx;
            el.mesh.position.x = Math.cos(angle) * el.radius;
            el.mesh.position.z = Math.sin(angle) * el.radius;
          });
        }
      } else if (this.currentTopicKey === 'heart') {
        // Pulsating heartbeat simulation
        const scaleFactor = 1 + Math.sin(elapsedTime * 4) * 0.04;
        this.currentModelGroup.scale.set(scaleFactor, scaleFactor, scaleFactor);
      } else if (this.currentTopicKey === 'dna') {
        // Subtle vertical undulating rotation
        this.currentModelGroup.rotation.y = elapsedTime * 0.4;
      } else if (this.currentTopicKey === 'solar_system') {
        const planets = this.currentModelGroup.userData.planets;
        if (planets) {
          planets.forEach(p => {
            const angle = elapsedTime * p.speed;
            p.mesh.position.x = Math.cos(angle) * p.distance;
            p.mesh.position.z = Math.sin(angle) * p.distance;
            p.mesh.rotation.y += 0.02;
          });
        }
      } else if (this.currentTopicKey === 'blockchain') {
        // Floating data cubes pulsation
        const cubes = this.currentModelGroup.userData.dataCubes;
        if (cubes) {
          cubes.forEach((c, idx) => {
            c.position.y = Math.sin(elapsedTime * 2 + idx) * 0.4;
            c.rotation.x += 0.01;
            c.rotation.y += 0.01;
          });
        }
      }
    }

    this.renderer.render(this.scene, this.camera);
  }

  loadModel(topicKey) {
    const item = this.registry[topicKey];
    if (!item) return;

    this.currentTopicKey = topicKey;

    // Show loading spinner
    this.toggleLoading(true);

    // Remove previous model group
    if (this.currentModelGroup) {
      this.scene.remove(this.currentModelGroup);
      this.disposeObject(this.currentModelGroup);
      this.currentModelGroup = null;
    }

    setTimeout(() => {
      // Build 3D mesh structure
      this.currentModelGroup = item.builder();
      this.scene.add(this.currentModelGroup);

      // Reset camera
      this.resetCamera();

      // Update info cards
      this.updateInfoPanel(item);

      this.toggleLoading(false);
    }, 120);
  }

  /* 1. Atom Model */
  buildAtomModel() {
    const group = new THREE.Group();

    // Central Nucleus (Protons & Neutrons clustered)
    const nucleusGroup = new THREE.Group();
    const pMat = new THREE.MeshPhongMaterial({ color: 0xef4444, shininess: 80, wireframe: this.isWireframe });
    const nMat = new THREE.MeshPhongMaterial({ color: 0x3b82f6, shininess: 80, wireframe: this.isWireframe });

    for (let i = 0; i < 14; i++) {
      const isProton = i % 2 === 0;
      const sphere = new THREE.Mesh(new THREE.SphereGeometry(0.35, 16, 16), isProton ? pMat : nMat);
      const phi = Math.acos(-1 + (2 * i) / 14);
      const theta = Math.sqrt(14 * Math.PI) * phi;
      sphere.position.set(
        Math.cos(theta) * Math.sin(phi) * 0.7,
        Math.sin(theta) * Math.sin(phi) * 0.7,
        Math.cos(phi) * 0.7
      );
      nucleusGroup.add(sphere);
    }
    group.add(nucleusGroup);

    // Electron Shells (Orbits)
    const orbitRadii = [2.8, 4.5, 6.2];
    const orbitRotations = [
      { x: Math.PI / 4, y: 0, z: 0 },
      { x: -Math.PI / 4, y: Math.PI / 3, z: 0 },
      { x: 0, y: -Math.PI / 3, z: Math.PI / 4 }
    ];

    const electronList = [];
    const eMat = new THREE.MeshBasicMaterial({ color: 0x00c9a7 });

    orbitRadii.forEach((r, idx) => {
      // Ring
      const ringGeo = new THREE.RingGeometry(r - 0.03, r + 0.03, 64);
      const ringMat = new THREE.MeshBasicMaterial({ color: 0x6c63ff, side: THREE.DoubleSide, transparent: true, opacity: 0.6 });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.rotation.x = Math.PI / 2;
      
      const orbitPivot = new THREE.Group();
      orbitPivot.rotation.set(orbitRotations[idx].x, orbitRotations[idx].y, orbitRotations[idx].z);
      orbitPivot.add(ring);

      // Electron particle
      const electron = new THREE.Mesh(new THREE.SphereGeometry(0.18, 16, 16), eMat);
      electron.position.set(r, 0, 0);
      orbitPivot.add(electron);

      electronList.push({ mesh: electron, radius: r });
      group.add(orbitPivot);
    });

    group.userData.electrons = electronList;
    return group;
  }

  /* 2. DNA Helix Model */
  buildDNAModel() {
    const group = new THREE.Group();
    const pairsCount = 36;
    const radius = 1.8;
    const heightStep = 0.32;
    const angleStep = 0.35;

    const strand1Mat = new THREE.MeshPhongMaterial({ color: 0x6c63ff, shininess: 90, wireframe: this.isWireframe });
    const strand2Mat = new THREE.MeshPhongMaterial({ color: 0x00c9a7, shininess: 90, wireframe: this.isWireframe });
    const rungMat1 = new THREE.MeshPhongMaterial({ color: 0xffb800 });
    const rungMat2 = new THREE.MeshPhongMaterial({ color: 0xff6584 });

    const totalHeight = pairsCount * heightStep;
    const startY = -totalHeight / 2;

    for (let i = 0; i < pairsCount; i++) {
      const angle = i * angleStep;
      const y = startY + i * heightStep;

      // Backbone node 1
      const x1 = Math.cos(angle) * radius;
      const z1 = Math.sin(angle) * radius;
      const node1 = new THREE.Mesh(new THREE.SphereGeometry(0.22, 16, 16), strand1Mat);
      node1.position.set(x1, y, z1);
      group.add(node1);

      // Backbone node 2 (opposite angle)
      const x2 = Math.cos(angle + Math.PI) * radius;
      const z2 = Math.sin(angle + Math.PI) * radius;
      const node2 = new THREE.Mesh(new THREE.SphereGeometry(0.22, 16, 16), strand2Mat);
      node2.position.set(x2, y, z2);
      group.add(node2);

      // Connecting Base Rung
      const rungDist = radius * 2;
      const rungGeo = new THREE.CylinderGeometry(0.08, 0.08, rungDist, 12);
      const rung = new THREE.Mesh(rungGeo, i % 2 === 0 ? rungMat1 : rungMat2);
      rung.position.set(0, y, 0);
      rung.rotation.z = Math.PI / 2;
      rung.rotation.y = -angle;
      group.add(rung);
    }

    return group;
  }

  /* 3. Human Heart Model */
  buildHeartModel() {
    const group = new THREE.Group();

    // Muscle body (anatomical dual bulb ventricles)
    const muscleMat = new THREE.MeshPhongMaterial({ color: 0xef4444, shininess: 60, wireframe: this.isWireframe });
    const blueMat = new THREE.MeshPhongMaterial({ color: 0x2563eb, shininess: 70 });
    const aortaMat = new THREE.MeshPhongMaterial({ color: 0xd97706, shininess: 70 });

    // Left ventricle
    const leftV = new THREE.Mesh(new THREE.SphereGeometry(1.8, 32, 32), muscleMat);
    leftV.scale.set(1, 1.4, 0.9);
    leftV.position.set(-0.6, -0.4, 0);
    group.add(leftV);

    // Right ventricle
    const rightV = new THREE.Mesh(new THREE.SphereGeometry(1.6, 32, 32), muscleMat);
    rightV.scale.set(0.9, 1.3, 0.85);
    rightV.position.set(0.7, -0.3, 0.2);
    group.add(rightV);

    // Aorta Arch (Torus tube)
    const aortaGeo = new THREE.TorusGeometry(1.2, 0.35, 16, 32, Math.PI * 0.9);
    const aorta = new THREE.Mesh(aortaGeo, aortaMat);
    aorta.position.set(-0.3, 1.4, 0);
    aorta.rotation.z = -0.3;
    group.add(aorta);

    // Pulmonary Trunk / Artery
    const pulGeo = new THREE.CylinderGeometry(0.35, 0.35, 2.2, 16);
    const pulmonary = new THREE.Mesh(pulGeo, blueMat);
    pulmonary.position.set(0.6, 1.2, -0.2);
    pulmonary.rotation.z = 0.4;
    group.add(pulmonary);

    // Vena Cava
    const venaGeo = new THREE.CylinderGeometry(0.3, 0.3, 1.8, 16);
    const vena = new THREE.Mesh(venaGeo, blueMat);
    vena.position.set(1.4, 0.6, -0.4);
    group.add(vena);

    return group;
  }

  /* 4. Human Brain Model */
  buildBrainModel() {
    const group = new THREE.Group();
    const brainMatLeft = new THREE.MeshPhongMaterial({ color: 0xec4899, shininess: 50, wireframe: this.isWireframe });
    const brainMatRight = new THREE.MeshPhongMaterial({ color: 0xa855f7, shininess: 50, wireframe: this.isWireframe });

    // Left hemisphere with surface gyri bumps
    const leftH = new THREE.Mesh(new THREE.SphereGeometry(1.9, 32, 32), brainMatLeft);
    leftH.scale.set(0.9, 1.1, 1.4);
    leftH.position.set(-0.95, 0, 0);
    group.add(leftH);

    // Right hemisphere
    const rightH = new THREE.Mesh(new THREE.SphereGeometry(1.9, 32, 32), brainMatRight);
    rightH.scale.set(0.9, 1.1, 1.4);
    rightH.position.set(0.95, 0, 0);
    group.add(rightH);

    // Cerebellum
    const cbMat = new THREE.MeshPhongMaterial({ color: 0xf43f5e, shininess: 40 });
    const cerebellum = new THREE.Mesh(new THREE.SphereGeometry(1.1, 24, 24), cbMat);
    cerebellum.scale.set(1.4, 0.7, 0.9);
    cerebellum.position.set(0, -1.3, -1.2);
    group.add(cerebellum);

    // Brainstem
    const stemMat = new THREE.MeshPhongMaterial({ color: 0xe2e8f0 });
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.3, 1.8, 16), stemMat);
    stem.position.set(0, -2.0, -0.6);
    group.add(stem);

    return group;
  }

  /* 5. Solar System Model */
  buildSolarSystemModel() {
    const group = new THREE.Group();

    // Central Sun
    const sunMat = new THREE.MeshBasicMaterial({ color: 0xffb800 });
    const sun = new THREE.Mesh(new THREE.SphereGeometry(1.6, 32, 32), sunMat);
    group.add(sun);

    // Coronal Glow Halo
    const haloGeo = new THREE.SphereGeometry(2.1, 24, 24);
    const haloMat = new THREE.MeshBasicMaterial({ color: 0xffa500, transparent: true, opacity: 0.25 });
    group.add(new THREE.Mesh(haloGeo, haloMat));

    const planetDefs = [
      { name: 'Mercury', color: 0x94a3b8, size: 0.2, dist: 3.0, speed: 1.6 },
      { name: 'Venus', color: 0xf59e0b, size: 0.35, dist: 4.4, speed: 1.2 },
      { name: 'Earth', color: 0x3b82f6, size: 0.38, dist: 6.0, speed: 0.9 },
      { name: 'Mars', color: 0xef4444, size: 0.28, dist: 7.8, speed: 0.7 },
      { name: 'Jupiter', color: 0xd97706, size: 0.85, dist: 10.2, speed: 0.4 },
      { name: 'Saturn', color: 0xfde047, size: 0.7, dist: 12.8, speed: 0.3, hasRings: true }
    ];

    const planetList = [];

    planetDefs.forEach(p => {
      // Orbital Ring Trace
      const ringGeo = new THREE.RingGeometry(p.dist - 0.02, p.dist + 0.02, 64);
      const ringMat = new THREE.MeshBasicMaterial({ color: 0x334155, side: THREE.DoubleSide });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.rotation.x = Math.PI / 2;
      group.add(ring);

      // Planet Mesh
      const pMesh = new THREE.Mesh(new THREE.SphereGeometry(p.size, 20, 20), new THREE.MeshPhongMaterial({ color: p.color }));
      pMesh.position.set(p.dist, 0, 0);
      group.add(pMesh);

      // Saturn Rings
      if (p.hasRings) {
        const sRingGeo = new THREE.RingGeometry(p.size * 1.4, p.size * 2.3, 32);
        const sRingMat = new THREE.MeshBasicMaterial({ color: 0xca8a04, side: THREE.DoubleSide });
        const sRing = new THREE.Mesh(sRingGeo, sRingMat);
        sRing.rotation.x = Math.PI / 2.5;
        pMesh.add(sRing);
      }

      planetList.push({ mesh: pMesh, distance: p.dist, speed: p.speed });
    });

    group.userData.planets = planetList;
    return group;
  }

  /* 6. CPU Chip Architecture Model */
  buildCPUModel() {
    const group = new THREE.Group();

    // Green PCB Substrate
    const pcbMat = new THREE.MeshPhongMaterial({ color: 0x065f46, shininess: 40 });
    const pcb = new THREE.Mesh(new THREE.BoxGeometry(6.5, 0.3, 6.5), pcbMat);
    group.add(pcb);

    // Gold Pin Grid Underneath
    const pinMat = new THREE.MeshPhongMaterial({ color: 0xeab308, shininess: 90 });
    for (let x = -2.8; x <= 2.8; x += 0.8) {
      for (let z = -2.8; z <= 2.8; z += 0.8) {
        const pin = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.4, 8), pinMat);
        pin.position.set(x, -0.3, z);
        group.add(pin);
      }
    }

    // Silicon Die / Integrated Heat Spreader (IHS)
    const ihsMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.8, roughness: 0.2 });
    const ihs = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.4, 4.5), ihsMat);
    ihs.position.set(0, 0.35, 0);
    group.add(ihs);

    // 4 CPU Multi-Cores
    const coreMat = new THREE.MeshPhongMaterial({ color: 0x6c63ff, shininess: 80 });
    const coreCoords = [
      { x: -1.1, z: -1.1 }, { x: 1.1, z: -1.1 },
      { x: -1.1, z: 1.1 }, { x: 1.1, z: 1.1 }
    ];
    coreCoords.forEach(c => {
      const core = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.1, 1.7), coreMat);
      core.position.set(c.x, 0.6, c.z);
      group.add(core);
    });

    return group;
  }

  /* 7. Network Star Topology Model */
  buildNetworkModel() {
    const group = new THREE.Group();

    // Central Layer-3 Switch / Hub
    const switchMat = new THREE.MeshPhongMaterial({ color: 0x6c63ff, shininess: 80 });
    const centralSwitch = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 0.6, 24), switchMat);
    group.add(centralSwitch);

    // Indicator LEDs
    const ledMat = new THREE.MeshBasicMaterial({ color: 0x00c9a7 });
    for (let i = 0; i < 6; i++) {
      const led = new THREE.Mesh(new THREE.SphereGeometry(0.1, 8, 8), ledMat);
      const a = (i * Math.PI) / 3;
      led.position.set(Math.cos(a) * 1.3, 0.2, Math.sin(a) * 1.3);
      group.add(led);
    }

    // 5 Client Nodes + 1 Server Node
    const clientMat = new THREE.MeshPhongMaterial({ color: 0x38bdf8 });
    const serverMat = new THREE.MeshPhongMaterial({ color: 0xec4899 });
    const cableMat = new THREE.MeshBasicMaterial({ color: 0x475569 });

    for (let i = 0; i < 6; i++) {
      const angle = (i * 2 * Math.PI) / 6;
      const radius = 5.5;
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;

      // Cable to Center
      const lineGeo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(x, 0, z)
      ]);
      const cable = new THREE.Line(lineGeo, cableMat);
      group.add(cable);

      if (i === 0) {
        // High Availability Server Rack
        const server = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.8, 1.0), serverMat);
        server.position.set(x, 0.5, z);
        group.add(server);
      } else {
        // Client Workstation Monitor & Base
        const client = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.7, 0.4), clientMat);
        client.position.set(x, 0.35, z);
        client.lookAt(0, 0, 0);
        group.add(client);
      }
    }

    return group;
  }

  /* 8. Blockchain 3D Ledger Model */
  buildBlockchainModel() {
    const group = new THREE.Group();

    const blockMat1 = new THREE.MeshPhongMaterial({ color: 0x1b2340, shininess: 80, wireframe: this.isWireframe });
    const borderMat = new THREE.MeshBasicMaterial({ color: 0x6c63ff, wireframe: true });
    const cableMat = new THREE.MeshBasicMaterial({ color: 0x00c9a7 });

    const blocks = [-4.0, 0, 4.0];
    const dataCubes = [];

    blocks.forEach((bx, idx) => {
      // Block Outer Body
      const block = new THREE.Mesh(new THREE.BoxGeometry(2.4, 2.6, 2.4), blockMat1);
      block.position.set(bx, 0, 0);
      group.add(block);

      const blockOutline = new THREE.Mesh(new THREE.BoxGeometry(2.45, 2.65, 2.45), borderMat);
      blockOutline.position.set(bx, 0, 0);
      group.add(blockOutline);

      // Inner Floating Data Payload Cube
      const dCubeMat = new THREE.MeshPhongMaterial({ color: idx === 1 ? 0x00c9a7 : 0xffb800 });
      const dCube = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.9, 0.9), dCubeMat);
      dCube.position.set(bx, 0, 0);
      group.add(dCube);
      dataCubes.push(dCube);

      // Connecting Hash Link Cable to next block
      if (idx < blocks.length - 1) {
        const nextX = blocks[idx + 1];
        const cylGeo = new THREE.CylinderGeometry(0.12, 0.12, nextX - bx, 16);
        const cable = new THREE.Mesh(cylGeo, cableMat);
        cable.position.set((bx + nextX) / 2, 0, 0);
        cable.rotation.z = Math.PI / 2;
        group.add(cable);
      }
    });

    group.userData.dataCubes = dataCubes;
    return group;
  }

  /* Control buttons setup */
  setupUIEvents() {
    // Topic Selector buttons
    const selectorBtns = document.querySelectorAll('[data-3d-topic]');
    selectorBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        selectorBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.loadModel(btn.getAttribute('data-3d-topic'));
      });
    });

    // Rotate Toggle
    const rotateBtn = document.getElementById('threeRotateToggleBtn');
    if (rotateBtn) {
      rotateBtn.addEventListener('click', () => {
        this.isAutoRotating = !this.isAutoRotating;
        rotateBtn.classList.toggle('active', this.isAutoRotating);
      });
    }

    // Wireframe Toggle
    const wireframeBtn = document.getElementById('threeWireframeBtn');
    if (wireframeBtn) {
      wireframeBtn.addEventListener('click', () => {
        this.isWireframe = !this.isWireframe;
        wireframeBtn.classList.toggle('active', this.isWireframe);
        // Reload current model to apply wireframe
        this.loadModel(this.currentTopicKey);
      });
    }

    // Zoom In
    const zoomInBtn = document.getElementById('threeZoomInBtn');
    if (zoomInBtn) {
      zoomInBtn.addEventListener('click', () => {
        this.camera.position.multiplyScalar(0.85);
      });
    }

    // Zoom Out
    const zoomOutBtn = document.getElementById('threeZoomOutBtn');
    if (zoomOutBtn) {
      zoomOutBtn.addEventListener('click', () => {
        this.camera.position.multiplyScalar(1.15);
      });
    }

    // Reset Camera
    const resetBtn = document.getElementById('threeResetBtn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => this.resetCamera());
    }

    // Fullscreen Toggle
    const fsBtn = document.getElementById('threeFullscreenBtn');
    if (fsBtn) {
      fsBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
          this.container.requestFullscreen().catch(err => console.error(err));
        } else {
          document.exitFullscreen();
        }
      });
    }
  }

  resetCamera() {
    if (this.camera && this.controls) {
      this.camera.position.set(0, 5, 14);
      this.controls.target.set(0, 0, 0);
      this.controls.update();
    }
  }

  updateInfoPanel(item) {
    const titleEl = document.getElementById('modelInfoTitle');
    const catEl = document.getElementById('modelInfoCategory');
    const descEl = document.getElementById('modelInfoDesc');
    const partsContainer = document.getElementById('modelPartsContainer');

    if (titleEl) titleEl.textContent = item.name;
    if (catEl) catEl.textContent = item.category;
    if (descEl) descEl.textContent = item.description;

    if (partsContainer) {
      partsContainer.innerHTML = item.parts.map((p, idx) => `
        <div class="p-2 px-3 rounded-3 mb-2" style="background-color: var(--bg-input); border: 1px solid var(--border-color);">
          <div class="fw-semibold text-primary small"><i class="bi bi-chevron-right me-1"></i> ${escapeHtml(p.name)}</div>
          <div class="text-muted small" style="font-size: 0.82rem;">${escapeHtml(p.desc)}</div>
        </div>
      `).join('');
    }
  }

  toggleLoading(show) {
    const spinner = document.getElementById('threeLoadingSpinner');
    if (spinner) {
      spinner.classList.toggle('d-none', !show);
    }
  }

  disposeObject(obj) {
    while (obj.children && obj.children.length > 0) {
      this.disposeObject(obj.children[0]);
      obj.remove(obj.children[0]);
    }
    if (obj.geometry) obj.geometry.dispose();
    if (obj.material) {
      if (Array.isArray(obj.material)) {
        obj.material.forEach(m => m.dispose());
      } else {
        obj.material.dispose();
      }
    }
  }
}

// Global initialization
window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('threeContainer')) {
    window.lab3d = new Interactive3DLab('threeContainer');
  }
});
