/*
* Sample script to compute bit stats of an integer number.
*/

Object.prototype.print = function(output) {
	Object.entries(this).forEach(
		([k, value]) => { output.log(k, " - ", value); }
	);
}

class Digits {
	static __SEQ = '0123456789abcedfghijklmopqrstuvwyz';

	constructor(radix) {
		this.__radix = radix;
		this.__digits = Digits.__SEQ.substring(0, radix);
		this.setUp();
	}

	setUp() {
		this.__t = new Map(
			this.__digits.split('')
				.map(
					(i) => { return [ parseInt(i, this.__radix), i ] }
				)
		);
		this.__stats = {};
		for (const d of this.__digits) {
			this.__stats[d] = 0;
		}
	}

	update(n) {
		this.__stats[n]++;
	}

	getStats() {
		return this.__stats;
	}
}

class Binary extends Digits {
	constructor() {
		super(2);
	}

	__bits(n) {
		let b = '';
		for (let i = n; ; i = i >> 1) {
			b = this.__t.get(i % 2) + b;
			if (i <= 0) break;
		}
		return b;
	}

	computeStats(n) {
		for (const b of this.__bits(n)) {
			this.update(b);
		}
		return this.getStats();
	}
}

let obj = new Binary();
obj.computeStats(0xfede).print(console);
