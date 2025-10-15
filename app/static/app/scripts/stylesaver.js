class Stylesaver {
	constructor(styles) {
		this.styles = styles;
		this.map = new WeakMap();
	}

	save(elem) {
		let styles = {};
		for (let style of this.styles) {
			styles[style] = elem.style[style];
		}
		this.map.set(elem, styles);
	}

	restore(elem) {
		let styles = this.map.get(elem);
		if (!styles) return;
		for (let [style, val] of Object.entries(styles)) {
			elem.style[style] = val;
		}
	}

	saveAndRestore(elem) {
		let savedStyles = this.map.get(elem);

		let styles = {};
		for (let style of this.styles) {
			styles[style] = elem.style[style];
		}
		this.map.set(elem, styles);

		for (let [style, val] of savedStyles.entries()) {
			elem.style[style] = val;
		}
	}
}

// export default Stylesaver;
// export {Stylesaver};

STYLESAVER_VERSION = "0.5";