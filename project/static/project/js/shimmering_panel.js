let field = document.getElementById("text-field");
state = {
	"boxShadow": null,
	"textShadow": null,
};
let count = 0;
let pulse = () => {
	for (let [key, value] of Object.entries(state)) {
		[state[key], field.style[key]] = [field.style[key], value];
	}
	count = (count - 1) * -1;
	let latency = Math.random() * (count ? 200 : 2000);

	setTimeout(pulse, latency);
};

setTimeout(pulse, Math.random() * 2000);