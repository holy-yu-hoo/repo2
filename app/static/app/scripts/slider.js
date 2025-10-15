"use strict";
// import Stylesaver from "./stylesaver";


export default class RangeSlider extends HTMLElement {

	static formAssociated = true;

	constructor() {
		super();
		this.internals = this.attachInternals();
		let shadow = this.attachShadow({mode: "closed"});
		shadow.innerHTML = this.defaultStyle;

		this.slider = document.createElement("div");
		this.slider.id = "slider";
		this.slider.setAttribute("part", "slider");
		this.slider.setAttribute("tabindex", "0");
		shadow.appendChild(this.slider);

		this.thumb = document.createElement("div");
		this.thumb.id = "thumb";
		this.thumb.setAttribute("part", "thumb");
		this.slider.append(this.thumb);


		this.input = document.createElement("input");
		this.input.setAttribute("type", "text");
		this.input.setAttribute("id", "input");
		this.input.setAttribute("part", "input");
		this.input.setAttribute("name", "range");
		this.input.setAttribute("tabindex", "-1");
		this.thumb.appendChild(this.input);

	}

	static get observedAttributes() {
		return ["step", "value"];
	}


	get form() { return this.internals.form; }

	get name() { return this.getAttribute("name"); }

	get type() { return this.localName; }

	get validity() {return this.internals.validity; }

	get validationMessage() {return this.internals.validationMessage; }

	get willValidate() {return this.internals.willValidate; }

	get value() {
		return parseInt(this._value);
	}

	set value(value) {
		value = parseInt(value);
		if (isNaN(value)) {
			this.value = this.value;
			return;
		}

		value = Math.max(0, value);
		value = Math.min(value, 100);

		this._value = (value / this.step).toFixed(0) * this.step;

		let x = this.value * (this.slider.offsetWidth - this.thumb.offsetWidth) / 100;
		this.thumb.style.left = x + "px";
		this.input.value = this.value.toString();
		this._updateBackground();
		this.internals.setFormValue(this.value.toString());
	}

	get step() {return this._step;}

	set step(value) { this._step = value; }

	get defaultStyle() {
		return `
				<style>
				@layer default {
					:host {
						width: 50%;
						max-width:400px;
						min-width: 200px;
						aspect-ratio: 10/1;
						max-height: 40px;
						min-height: 20px;
						display: block;
						touch-action: none;
					}
					#slider{ 
						width: 100%;
						height: 100%;
						border-radius: 25px;
						touch-action: none;
						outline: 5px solid black;
						position: relative;
						user-select: none;
						outline-offset: -5px;
					}

					#thumb{
						max-width: 40px;
						min-width: 20px;
						height: 100%;
						background-color: white;
						position: relative !important;
						border-radius: 20px;
						touch-action: none;
						aspect-ratio: 1/1;
						/* outline: 5px solid black; */
						/* outline-offset: -1px; */
						user-select: none;
					}
					#input{
						all: initial;
						width: 100%;
						height: 100%;
						text-align: center;
						touch-action: none;
						user-select: none;
						-webkit-touch-callout: none;
					}

					
				}
				</style>`;
	}

	get sliderRect() {
		return this.slider.getBoundingClientRect();
	}

	get thumbRect() {
		return this.thumb.getBoundingClientRect();
	}

	get colors() {
		//HSL
		return [
			{
				hue: 0,
				saturation: 100,
				lightness: 50,
			},
			{
				hue: 120,
				saturation: 100,
				lightness: 50,
			},
		];
	}

	checkValidity() { return this.internals.checkValidity(); }

	reportValidity() {return this.internals.reportValidity(); }

	attributeChangedCallback(name, oldValue, newValue) {
		name = name.replace(/-./g, s => s[1].toUpperCase()); //camelize
		this[name] = newValue;
	}

	connectedCallback() {
		if (!this.value) this.value = 0;
		if (!this.step) this.step = 1;

		this._onpointermove = this._onpointermove.bind(this);
		this._onpointerup = this._onpointerup.bind(this);
		this.slider.addEventListener("pointerdown", this._onpointerdown.bind(this));
		this.slider.addEventListener("wheel", this._onwheel.bind(this));
		this.addEventListener("keydown", this._onkeydown.bind(this));

		this.input.setAttribute("readonly", "readonly");
		this.input.addEventListener("dblclick", this._inputOnDblclick.bind(this));
		this.input.addEventListener("blur", this._inputOnBlur.bind(this));
		this.input.addEventListener("keydown", this._inputOnKeydown.bind(this));

		this.observer = new ResizeObserver((entries) => {
			for (let entry of entries) {
				let x = this.value * (this.sliderRect.width - this.thumbRect.width) / 100;
				this.thumb.style.left = x + "px";
			}
		});
		this.observer.observe(this);

	}


	_moveToddlerTo(clientX) {
		let x = clientX - this.sliderRect.left - this.shiftX;
		this.value = x / (this.sliderRect.width - this.thumbRect.width) * 100;
	}

	_updateBackground() {
		let perc = this.value / 100;
		let h = this.colors[0].hue + (this.colors[1].hue - this.colors[0].hue) * perc;
		let s = this.colors[0].saturation + (this.colors[1].saturation - this.colors[0].saturation) * perc;
		let l = this.colors[0].lightness + (this.colors[1].lightness - this.colors[0].lightness) * perc;
		this.slider.style.backgroundColor = `hsl(${h},${s}%,${l}%)`;

	}

	_onpointerdown(event) {
		if (event.target === this.thumb || event.target === this.input) {
			this.shiftX = event.clientX - this.thumbRect.left;
		} else if (event.target === this.slider) {
			this.shiftX = this.thumbRect.width / 2;
			this._moveToddlerTo(event.clientX);
		}
		event.target.focus();
		event.preventDefault();
		event.target.setPointerCapture(event.pointerId);
		this.slider.addEventListener("pointermove", this._onpointermove);
		this.slider.addEventListener("pointerup", this._onpointerup);
	}

	_onpointermove(event) {
		event.preventDefault();
		let x = event.clientX - this.sliderRect.left - this.shiftX;
		this.value = x / (this.sliderRect.width - this.thumbRect.width) * 100;

	}

	_onpointerup(event) {
		this.slider.removeEventListener("pointermove", this._onpointermove);
		this.slider.removeEventListener("pointerup", this._onpointerup);
		event.target.releasePointerCapture(event.pointerId);
	}

	_onwheel(event) {
		event.preventDefault();
		console.log(event);
		let value = Math.sign(event.deltaY) * -10;
		this.value += value;
	}

	_onkeydown(event) {
		if (event.key === "ArrowLeft") {
			this.value -= 10;
		} else if (event.key === "ArrowRight") {
			this.value += 10;
		}
	}


	_inputOnDblclick() {
		if (this.input.hasAttribute("readonly")) {
			this.input.removeAttribute("readonly");
			this.input.focus();
			this.input.select();
		}
	}

	_inputOnBlur() {
		if (!this.input.hasAttribute("readonly")) {
			this.input.setAttribute("readonly", "");
		}
	}

	_inputOnKeydown(event) {
		if (event.code === "Enter") {
			this.input.setAttribute("readonly", "");
			this.value = this.input.value;
		} else if (event.code === "Escape") {
			this.input.setAttribute("readonly", "");
			this.input.value = this.value.toString();
		}
	}


}

customElements.define("range-slider", RangeSlider);
