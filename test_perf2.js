function tryQR_apply(len) {
    const s=new Uint8Array(len);s.fill(65);
    return String.fromCharCode.apply(null, s);
}

function tryQR_repeat(len) {
    return 'A'.repeat(len);
}

console.time('apply');
for(let i=0; i<10000; i++) {
    tryQR_apply(8192);
}
console.timeEnd('apply');

console.time('repeat');
for(let i=0; i<10000; i++) {
    tryQR_repeat(8192);
}
console.timeEnd('repeat');
