// mock qrcode
function qrcode(version, ecc) {
    return {
        addData: function(str, type) {},
        make: function() {}
    };
}

function tryQR_old(version,ecc,len){const s=new Uint8Array(len);s.fill(65);let str='';for(let i=0;i<s.length;i++)str+=String.fromCharCode(s[i]);try{const q=qrcode(version,ecc);q.addData(str,'Byte');q.make();return true}catch(e){return false}}

function tryQR_new(version,ecc,len){const str='A'.repeat(len);try{const q=qrcode(version,ecc);q.addData(str,'Byte');q.make();return true}catch(e){return false}}

console.time('old');
for(let i=0; i<10000; i++) {
    tryQR_old(40, 'M', 8192);
}
console.timeEnd('old');

console.time('new');
for(let i=0; i<10000; i++) {
    tryQR_new(40, 'M', 8192);
}
console.timeEnd('new');
