class Player extends HTMLElement {
	constructor() {
		super();
		this.shadow=this.attachShadow({ mode: 'open' });
		this.audio=new Audio()
		this.__createPlayButton()


		this.audio.addEventListener('loadedmetadata', () => {
			console.log('Метаданные загружены:', this.audio.duration);
		});

		this.audio.addEventListener('canplay', () => {
			console.log('Аудио готово к воспроизведению');
		});

		this.audio.addEventListener('error', (e) => {
			console.error('Ошибка загрузки аудио:', e);
		});
	}

	connectedCallback() {
		console.log("Player connected");
	}

	static get observedAttributes() {
		return ["src","loop","autoplay","muted"];
	}

	static get src(){
		return this.audio.src;
	}

	static set src(nval){
		this.audio.src=nval;
	}
	attributeChangedCallback(name, oldValue, newValue) {
		console.log(newValue);
		this.audio[name] = newValue;
		if (name==="src"){ this.audio.load()}
	}

	__createPlayButton(){
		this.playButton=document.createElement("div");
		this.playButton.innerHTML='⏵︎';
		this.shadow.append(this.playButton);
		this.playButton.style.cssText=`
		font-height:20px;
		user-select:none;
		`
		this.playButton.addEventListener('click',()=>{
			if (this.audio.paused){
				this.playButton.innerHTML='⏸︎'
				this.audio.play().then(()=>{console.log("Player played!");})
			} else {
				this.playButton.innerHTML='⏵︎'
				this.audio.pause()
			}
		})
	}
}


customElements.define('audio-player', Player);