/*
* sample script to compute bit stats of an integer number.
*/

const DEFAULT_HEX_DIGITS = '0123456789abcedf';
const DEFAULT_BIN_DIGITS = '01';

let t = new Map(
	DEFAULT_BIN_DIGITS.split('').map((i) => {
		return [ parseInt(i), i ]
	})
);

let bits = function(n) {
	let b = '';
	for (i = n; ; i = i >> 1) {
		b = t.get(i % 2) + b;
		if (i <= 0) {
			break;
		}
	}
	return b;
}

let computeBinStats = function(n, digits = DEFAULT_BIN_DIGITS) {
	let stats = {};
	for (let c of bits(n)) {
		if (DEFAULT_BIN_DIGITS.includes(c)) {
				stats[c] = c in stats ? stats[c]+1 : 1;
		}
	}
	return stats;
}

let s = computeBinStats(0xbeef);
console.log(s);
