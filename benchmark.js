const fs = require('fs');

// mock crypto.getRandomValues using node's crypto
const nodeCrypto = require('crypto');
global.crypto = {
    getRandomValues: function(buffer) {
        const rand = nodeCrypto.randomBytes(buffer.length);
        buffer.set(rand);
        return buffer;
    }
};

// current code
function randSuffix(n){const chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';let s='';const max=Math.floor(256/chars.length)*chars.length;const a=new Uint8Array(1);for(let i=0;i<n;i++){do{crypto.getRandomValues(a)}while(a[0]>=max);s+=chars[a[0]%chars.length];}return s}

// proposed code
function randSuffixOptimized(n){const chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';let s='';const max=Math.floor(256/chars.length)*chars.length;const a=new Uint8Array(n);crypto.getRandomValues(a);let idx=0;for(let i=0;i<n;i++){let r;do{if(idx>=n){crypto.getRandomValues(a);idx=0}r=a[idx++];}while(r>=max);s+=chars[r%chars.length];}return s}

// bench
const ITERS = 100000;
const N = 32;

console.log("Benchmarking current implementation...");
console.time("current");
for (let i=0; i<ITERS; i++) {
    randSuffix(N);
}
console.timeEnd("current");

console.log("Benchmarking optimized implementation...");
console.time("optimized");
for (let i=0; i<ITERS; i++) {
    randSuffixOptimized(N);
}
console.timeEnd("optimized");
