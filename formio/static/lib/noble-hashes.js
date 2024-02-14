"use strict";
var nobleHashes = (() => {
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

  // input.js
  var input_exports = {};
  __export(input_exports, {
    argon2id: () => argon2id,
    blake2b: () => blake2b,
    blake2s: () => blake2s,
    blake3: () => blake3,
    cshake128: () => cshake128,
    cshake256: () => cshake256,
    eskdf: () => eskdf,
    hkdf: () => hkdf,
    hmac: () => hmac,
    k12: () => k12,
    keccak_224: () => keccak_224,
    keccak_256: () => keccak_256,
    keccak_384: () => keccak_384,
    keccak_512: () => keccak_512,
    kmac128: () => kmac128,
    kmac256: () => kmac256,
    m14: () => m14,
    pbkdf2: () => pbkdf2,
    pbkdf2Async: () => pbkdf2Async,
    ripemd160: () => ripemd160,
    scrypt: () => scrypt,
    scryptAsync: () => scryptAsync,
    sha1: () => sha1,
    sha256: () => sha256,
    sha3_224: () => sha3_224,
    sha3_256: () => sha3_256,
    sha3_384: () => sha3_384,
    sha3_512: () => sha3_512,
    sha512: () => sha512,
    utils: () => utils
  });

  // node_modules/@noble/hashes/esm/crypto.js
  var crypto = typeof globalThis === "object" && "crypto" in globalThis ? globalThis.crypto : void 0;

  // node_modules/@noble/hashes/esm/utils.js
  var u8 = (arr) => new Uint8Array(arr.buffer, arr.byteOffset, arr.byteLength);
  var u32 = (arr) => new Uint32Array(arr.buffer, arr.byteOffset, Math.floor(arr.byteLength / 4));
  function isBytes(a) {
    return a instanceof Uint8Array || a != null && typeof a === "object" && a.constructor.name === "Uint8Array";
  }
  var createView = (arr) => new DataView(arr.buffer, arr.byteOffset, arr.byteLength);
  var rotr = (word, shift) => word << 32 - shift | word >>> shift;
  var isLE = new Uint8Array(new Uint32Array([287454020]).buffer)[0] === 68;
  if (!isLE)
    throw new Error("Non little-endian hardware is not supported");
  var hexes = /* @__PURE__ */ Array.from({ length: 256 }, (_, i) => i.toString(16).padStart(2, "0"));
  function bytesToHex(bytes2) {
    if (!isBytes(bytes2))
      throw new Error("Uint8Array expected");
    let hex = "";
    for (let i = 0; i < bytes2.length; i++) {
      hex += hexes[bytes2[i]];
    }
    return hex;
  }
  var asciis = { _0: 48, _9: 57, _A: 65, _F: 70, _a: 97, _f: 102 };
  function asciiToBase16(char) {
    if (char >= asciis._0 && char <= asciis._9)
      return char - asciis._0;
    if (char >= asciis._A && char <= asciis._F)
      return char - (asciis._A - 10);
    if (char >= asciis._a && char <= asciis._f)
      return char - (asciis._a - 10);
    return;
  }
  function hexToBytes(hex) {
    if (typeof hex !== "string")
      throw new Error("hex string expected, got " + typeof hex);
    const hl = hex.length;
    const al = hl / 2;
    if (hl % 2)
      throw new Error("padded hex string expected, got unpadded hex of length " + hl);
    const array = new Uint8Array(al);
    for (let ai = 0, hi = 0; ai < al; ai++, hi += 2) {
      const n1 = asciiToBase16(hex.charCodeAt(hi));
      const n2 = asciiToBase16(hex.charCodeAt(hi + 1));
      if (n1 === void 0 || n2 === void 0) {
        const char = hex[hi] + hex[hi + 1];
        throw new Error('hex string expected, got non-hex character "' + char + '" at index ' + hi);
      }
      array[ai] = n1 * 16 + n2;
    }
    return array;
  }
  var nextTick = async () => {
  };
  async function asyncLoop(iters, tick, cb) {
    let ts = Date.now();
    for (let i = 0; i < iters; i++) {
      cb(i);
      const diff = Date.now() - ts;
      if (diff >= 0 && diff < tick)
        continue;
      await nextTick();
      ts += diff;
    }
  }
  function utf8ToBytes(str) {
    if (typeof str !== "string")
      throw new Error(`utf8ToBytes expected string, got ${typeof str}`);
    return new Uint8Array(new TextEncoder().encode(str));
  }
  function toBytes(data) {
    if (typeof data === "string")
      data = utf8ToBytes(data);
    if (!isBytes(data))
      throw new Error(`expected Uint8Array, got ${typeof data}`);
    return data;
  }
  var Hash = class {
    // Safe version that clones internal state
    clone() {
      return this._cloneInto();
    }
  };
  var toStr = {}.toString;
  function checkOpts(defaults, opts) {
    if (opts !== void 0 && toStr.call(opts) !== "[object Object]")
      throw new Error("Options should be object or undefined");
    const merged = Object.assign(defaults, opts);
    return merged;
  }
  function wrapConstructor(hashCons) {
    const hashC = (msg) => hashCons().update(toBytes(msg)).digest();
    const tmp = hashCons();
    hashC.outputLen = tmp.outputLen;
    hashC.blockLen = tmp.blockLen;
    hashC.create = () => hashCons();
    return hashC;
  }
  function wrapConstructorWithOpts(hashCons) {
    const hashC = (msg, opts) => hashCons(opts).update(toBytes(msg)).digest();
    const tmp = hashCons({});
    hashC.outputLen = tmp.outputLen;
    hashC.blockLen = tmp.blockLen;
    hashC.create = (opts) => hashCons(opts);
    return hashC;
  }
  function wrapXOFConstructorWithOpts(hashCons) {
    const hashC = (msg, opts) => hashCons(opts).update(toBytes(msg)).digest();
    const tmp = hashCons({});
    hashC.outputLen = tmp.outputLen;
    hashC.blockLen = tmp.blockLen;
    hashC.create = (opts) => hashCons(opts);
    return hashC;
  }
  function randomBytes(bytesLength = 32) {
    if (crypto && typeof crypto.getRandomValues === "function") {
      return crypto.getRandomValues(new Uint8Array(bytesLength));
    }
    throw new Error("crypto.getRandomValues must be defined");
  }

  // node_modules/@noble/hashes/esm/_assert.js
  function number(n) {
    if (!Number.isSafeInteger(n) || n < 0)
      throw new Error(`Wrong positive integer: ${n}`);
  }
  function isBytes2(a) {
    return a instanceof Uint8Array || a != null && typeof a === "object" && a.constructor.name === "Uint8Array";
  }
  function bytes(b, ...lengths) {
    if (!isBytes2(b))
      throw new Error("Expected Uint8Array");
    if (lengths.length > 0 && !lengths.includes(b.length))
      throw new Error(`Expected Uint8Array of length ${lengths}, not of length=${b.length}`);
  }
  function hash(hash2) {
    if (typeof hash2 !== "function" || typeof hash2.create !== "function")
      throw new Error("Hash should be wrapped by utils.wrapConstructor");
    number(hash2.outputLen);
    number(hash2.blockLen);
  }
  function exists(instance, checkFinished = true) {
    if (instance.destroyed)
      throw new Error("Hash instance has been destroyed");
    if (checkFinished && instance.finished)
      throw new Error("Hash#digest() has already been called");
  }
  function output(out, instance) {
    bytes(out);
    const min = instance.outputLen;
    if (out.length < min) {
      throw new Error(`digestInto() expects output buffer of length at least ${min}`);
    }
  }

  // node_modules/@noble/hashes/esm/_blake2.js
  var SIGMA = /* @__PURE__ */ new Uint8Array([
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    14,
    10,
    4,
    8,
    9,
    15,
    13,
    6,
    1,
    12,
    0,
    2,
    11,
    7,
    5,
    3,
    11,
    8,
    12,
    0,
    5,
    2,
    15,
    13,
    10,
    14,
    3,
    6,
    7,
    1,
    9,
    4,
    7,
    9,
    3,
    1,
    13,
    12,
    11,
    14,
    2,
    6,
    5,
    10,
    4,
    0,
    15,
    8,
    9,
    0,
    5,
    7,
    2,
    4,
    10,
    15,
    14,
    1,
    11,
    12,
    6,
    8,
    3,
    13,
    2,
    12,
    6,
    10,
    0,
    11,
    8,
    3,
    4,
    13,
    7,
    5,
    15,
    14,
    1,
    9,
    12,
    5,
    1,
    15,
    14,
    13,
    4,
    10,
    0,
    7,
    6,
    3,
    9,
    2,
    8,
    11,
    13,
    11,
    7,
    14,
    12,
    1,
    3,
    9,
    5,
    0,
    15,
    4,
    8,
    6,
    2,
    10,
    6,
    15,
    14,
    9,
    11,
    3,
    0,
    8,
    12,
    2,
    13,
    7,
    1,
    4,
    10,
    5,
    10,
    2,
    8,
    4,
    7,
    6,
    1,
    5,
    15,
    11,
    9,
    14,
    3,
    12,
    13,
    0,
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    14,
    10,
    4,
    8,
    9,
    15,
    13,
    6,
    1,
    12,
    0,
    2,
    11,
    7,
    5,
    3
  ]);
  var BLAKE2 = class extends Hash {
    constructor(blockLen, outputLen, opts = {}, keyLen, saltLen, persLen) {
      super();
      this.blockLen = blockLen;
      this.outputLen = outputLen;
      this.length = 0;
      this.pos = 0;
      this.finished = false;
      this.destroyed = false;
      number(blockLen);
      number(outputLen);
      number(keyLen);
      if (outputLen < 0 || outputLen > keyLen)
        throw new Error("outputLen bigger than keyLen");
      if (opts.key !== void 0 && (opts.key.length < 1 || opts.key.length > keyLen))
        throw new Error(`key must be up 1..${keyLen} byte long or undefined`);
      if (opts.salt !== void 0 && opts.salt.length !== saltLen)
        throw new Error(`salt must be ${saltLen} byte long or undefined`);
      if (opts.personalization !== void 0 && opts.personalization.length !== persLen)
        throw new Error(`personalization must be ${persLen} byte long or undefined`);
      this.buffer32 = u32(this.buffer = new Uint8Array(blockLen));
    }
    update(data) {
      exists(this);
      const { blockLen, buffer, buffer32 } = this;
      data = toBytes(data);
      const len = data.length;
      const offset = data.byteOffset;
      const buf = data.buffer;
      for (let pos = 0; pos < len; ) {
        if (this.pos === blockLen) {
          this.compress(buffer32, 0, false);
          this.pos = 0;
        }
        const take = Math.min(blockLen - this.pos, len - pos);
        const dataOffset = offset + pos;
        if (take === blockLen && !(dataOffset % 4) && pos + take < len) {
          const data32 = new Uint32Array(buf, dataOffset, Math.floor((len - pos) / 4));
          for (let pos32 = 0; pos + blockLen < len; pos32 += buffer32.length, pos += blockLen) {
            this.length += blockLen;
            this.compress(data32, pos32, false);
          }
          continue;
        }
        buffer.set(data.subarray(pos, pos + take), this.pos);
        this.pos += take;
        this.length += take;
        pos += take;
      }
      return this;
    }
    digestInto(out) {
      exists(this);
      output(out, this);
      const { pos, buffer32 } = this;
      this.finished = true;
      this.buffer.subarray(pos).fill(0);
      this.compress(buffer32, 0, true);
      const out32 = u32(out);
      this.get().forEach((v, i) => out32[i] = v);
    }
    digest() {
      const { buffer, outputLen } = this;
      this.digestInto(buffer);
      const res = buffer.slice(0, outputLen);
      this.destroy();
      return res;
    }
    _cloneInto(to) {
      const { buffer, length, finished, destroyed, outputLen, pos } = this;
      to || (to = new this.constructor({ dkLen: outputLen }));
      to.set(...this.get());
      to.length = length;
      to.finished = finished;
      to.destroyed = destroyed;
      to.outputLen = outputLen;
      to.buffer.set(buffer);
      to.pos = pos;
      return to;
    }
  };

  // node_modules/@noble/hashes/esm/_u64.js
  var U32_MASK64 = /* @__PURE__ */ BigInt(2 ** 32 - 1);
  var _32n = /* @__PURE__ */ BigInt(32);
  function fromBig(n, le = false) {
    if (le)
      return { h: Number(n & U32_MASK64), l: Number(n >> _32n & U32_MASK64) };
    return { h: Number(n >> _32n & U32_MASK64) | 0, l: Number(n & U32_MASK64) | 0 };
  }
  function split(lst, le = false) {
    let Ah = new Uint32Array(lst.length);
    let Al = new Uint32Array(lst.length);
    for (let i = 0; i < lst.length; i++) {
      const { h, l } = fromBig(lst[i], le);
      [Ah[i], Al[i]] = [h, l];
    }
    return [Ah, Al];
  }
  var toBig = (h, l) => BigInt(h >>> 0) << _32n | BigInt(l >>> 0);
  var shrSH = (h, _l, s) => h >>> s;
  var shrSL = (h, l, s) => h << 32 - s | l >>> s;
  var rotrSH = (h, l, s) => h >>> s | l << 32 - s;
  var rotrSL = (h, l, s) => h << 32 - s | l >>> s;
  var rotrBH = (h, l, s) => h << 64 - s | l >>> s - 32;
  var rotrBL = (h, l, s) => h >>> s - 32 | l << 64 - s;
  var rotr32H = (_h, l) => l;
  var rotr32L = (h, _l) => h;
  var rotlSH = (h, l, s) => h << s | l >>> 32 - s;
  var rotlSL = (h, l, s) => l << s | h >>> 32 - s;
  var rotlBH = (h, l, s) => l << s - 32 | h >>> 64 - s;
  var rotlBL = (h, l, s) => h << s - 32 | l >>> 64 - s;
  function add(Ah, Al, Bh, Bl) {
    const l = (Al >>> 0) + (Bl >>> 0);
    return { h: Ah + Bh + (l / 2 ** 32 | 0) | 0, l: l | 0 };
  }
  var add3L = (Al, Bl, Cl) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0);
  var add3H = (low, Ah, Bh, Ch) => Ah + Bh + Ch + (low / 2 ** 32 | 0) | 0;
  var add4L = (Al, Bl, Cl, Dl) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0) + (Dl >>> 0);
  var add4H = (low, Ah, Bh, Ch, Dh) => Ah + Bh + Ch + Dh + (low / 2 ** 32 | 0) | 0;
  var add5L = (Al, Bl, Cl, Dl, El) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0) + (Dl >>> 0) + (El >>> 0);
  var add5H = (low, Ah, Bh, Ch, Dh, Eh) => Ah + Bh + Ch + Dh + Eh + (low / 2 ** 32 | 0) | 0;
  var u64 = {
    fromBig,
    split,
    toBig,
    shrSH,
    shrSL,
    rotrSH,
    rotrSL,
    rotrBH,
    rotrBL,
    rotr32H,
    rotr32L,
    rotlSH,
    rotlSL,
    rotlBH,
    rotlBL,
    add,
    add3L,
    add3H,
    add4L,
    add4H,
    add5H,
    add5L
  };
  var u64_default = u64;

  // node_modules/@noble/hashes/esm/blake2b.js
  var IV = /* @__PURE__ */ new Uint32Array([
    4089235720,
    1779033703,
    2227873595,
    3144134277,
    4271175723,
    1013904242,
    1595750129,
    2773480762,
    2917565137,
    1359893119,
    725511199,
    2600822924,
    4215389547,
    528734635,
    327033209,
    1541459225
  ]);
  var BUF = /* @__PURE__ */ new Uint32Array(32);
  function G1(a, b, c, d, msg, x) {
    const Xl = msg[x], Xh = msg[x + 1];
    let Al = BUF[2 * a], Ah = BUF[2 * a + 1];
    let Bl = BUF[2 * b], Bh = BUF[2 * b + 1];
    let Cl = BUF[2 * c], Ch = BUF[2 * c + 1];
    let Dl = BUF[2 * d], Dh = BUF[2 * d + 1];
    let ll = u64_default.add3L(Al, Bl, Xl);
    Ah = u64_default.add3H(ll, Ah, Bh, Xh);
    Al = ll | 0;
    ({ Dh, Dl } = { Dh: Dh ^ Ah, Dl: Dl ^ Al });
    ({ Dh, Dl } = { Dh: u64_default.rotr32H(Dh, Dl), Dl: u64_default.rotr32L(Dh, Dl) });
    ({ h: Ch, l: Cl } = u64_default.add(Ch, Cl, Dh, Dl));
    ({ Bh, Bl } = { Bh: Bh ^ Ch, Bl: Bl ^ Cl });
    ({ Bh, Bl } = { Bh: u64_default.rotrSH(Bh, Bl, 24), Bl: u64_default.rotrSL(Bh, Bl, 24) });
    BUF[2 * a] = Al, BUF[2 * a + 1] = Ah;
    BUF[2 * b] = Bl, BUF[2 * b + 1] = Bh;
    BUF[2 * c] = Cl, BUF[2 * c + 1] = Ch;
    BUF[2 * d] = Dl, BUF[2 * d + 1] = Dh;
  }
  function G2(a, b, c, d, msg, x) {
    const Xl = msg[x], Xh = msg[x + 1];
    let Al = BUF[2 * a], Ah = BUF[2 * a + 1];
    let Bl = BUF[2 * b], Bh = BUF[2 * b + 1];
    let Cl = BUF[2 * c], Ch = BUF[2 * c + 1];
    let Dl = BUF[2 * d], Dh = BUF[2 * d + 1];
    let ll = u64_default.add3L(Al, Bl, Xl);
    Ah = u64_default.add3H(ll, Ah, Bh, Xh);
    Al = ll | 0;
    ({ Dh, Dl } = { Dh: Dh ^ Ah, Dl: Dl ^ Al });
    ({ Dh, Dl } = { Dh: u64_default.rotrSH(Dh, Dl, 16), Dl: u64_default.rotrSL(Dh, Dl, 16) });
    ({ h: Ch, l: Cl } = u64_default.add(Ch, Cl, Dh, Dl));
    ({ Bh, Bl } = { Bh: Bh ^ Ch, Bl: Bl ^ Cl });
    ({ Bh, Bl } = { Bh: u64_default.rotrBH(Bh, Bl, 63), Bl: u64_default.rotrBL(Bh, Bl, 63) });
    BUF[2 * a] = Al, BUF[2 * a + 1] = Ah;
    BUF[2 * b] = Bl, BUF[2 * b + 1] = Bh;
    BUF[2 * c] = Cl, BUF[2 * c + 1] = Ch;
    BUF[2 * d] = Dl, BUF[2 * d + 1] = Dh;
  }
  var BLAKE2b = class extends BLAKE2 {
    constructor(opts = {}) {
      super(128, opts.dkLen === void 0 ? 64 : opts.dkLen, opts, 64, 16, 16);
      this.v0l = IV[0] | 0;
      this.v0h = IV[1] | 0;
      this.v1l = IV[2] | 0;
      this.v1h = IV[3] | 0;
      this.v2l = IV[4] | 0;
      this.v2h = IV[5] | 0;
      this.v3l = IV[6] | 0;
      this.v3h = IV[7] | 0;
      this.v4l = IV[8] | 0;
      this.v4h = IV[9] | 0;
      this.v5l = IV[10] | 0;
      this.v5h = IV[11] | 0;
      this.v6l = IV[12] | 0;
      this.v6h = IV[13] | 0;
      this.v7l = IV[14] | 0;
      this.v7h = IV[15] | 0;
      const keyLength = opts.key ? opts.key.length : 0;
      this.v0l ^= this.outputLen | keyLength << 8 | 1 << 16 | 1 << 24;
      if (opts.salt) {
        const salt = u32(toBytes(opts.salt));
        this.v4l ^= salt[0];
        this.v4h ^= salt[1];
        this.v5l ^= salt[2];
        this.v5h ^= salt[3];
      }
      if (opts.personalization) {
        const pers = u32(toBytes(opts.personalization));
        this.v6l ^= pers[0];
        this.v6h ^= pers[1];
        this.v7l ^= pers[2];
        this.v7h ^= pers[3];
      }
      if (opts.key) {
        const tmp = new Uint8Array(this.blockLen);
        tmp.set(toBytes(opts.key));
        this.update(tmp);
      }
    }
    // prettier-ignore
    get() {
      let { v0l, v0h, v1l, v1h, v2l, v2h, v3l, v3h, v4l, v4h, v5l, v5h, v6l, v6h, v7l, v7h } = this;
      return [v0l, v0h, v1l, v1h, v2l, v2h, v3l, v3h, v4l, v4h, v5l, v5h, v6l, v6h, v7l, v7h];
    }
    // prettier-ignore
    set(v0l, v0h, v1l, v1h, v2l, v2h, v3l, v3h, v4l, v4h, v5l, v5h, v6l, v6h, v7l, v7h) {
      this.v0l = v0l | 0;
      this.v0h = v0h | 0;
      this.v1l = v1l | 0;
      this.v1h = v1h | 0;
      this.v2l = v2l | 0;
      this.v2h = v2h | 0;
      this.v3l = v3l | 0;
      this.v3h = v3h | 0;
      this.v4l = v4l | 0;
      this.v4h = v4h | 0;
      this.v5l = v5l | 0;
      this.v5h = v5h | 0;
      this.v6l = v6l | 0;
      this.v6h = v6h | 0;
      this.v7l = v7l | 0;
      this.v7h = v7h | 0;
    }
    compress(msg, offset, isLast) {
      this.get().forEach((v, i) => BUF[i] = v);
      BUF.set(IV, 16);
      let { h, l } = u64_default.fromBig(BigInt(this.length));
      BUF[24] = IV[8] ^ l;
      BUF[25] = IV[9] ^ h;
      if (isLast) {
        BUF[28] = ~BUF[28];
        BUF[29] = ~BUF[29];
      }
      let j = 0;
      const s = SIGMA;
      for (let i = 0; i < 12; i++) {
        G1(0, 4, 8, 12, msg, offset + 2 * s[j++]);
        G2(0, 4, 8, 12, msg, offset + 2 * s[j++]);
        G1(1, 5, 9, 13, msg, offset + 2 * s[j++]);
        G2(1, 5, 9, 13, msg, offset + 2 * s[j++]);
        G1(2, 6, 10, 14, msg, offset + 2 * s[j++]);
        G2(2, 6, 10, 14, msg, offset + 2 * s[j++]);
        G1(3, 7, 11, 15, msg, offset + 2 * s[j++]);
        G2(3, 7, 11, 15, msg, offset + 2 * s[j++]);
        G1(0, 5, 10, 15, msg, offset + 2 * s[j++]);
        G2(0, 5, 10, 15, msg, offset + 2 * s[j++]);
        G1(1, 6, 11, 12, msg, offset + 2 * s[j++]);
        G2(1, 6, 11, 12, msg, offset + 2 * s[j++]);
        G1(2, 7, 8, 13, msg, offset + 2 * s[j++]);
        G2(2, 7, 8, 13, msg, offset + 2 * s[j++]);
        G1(3, 4, 9, 14, msg, offset + 2 * s[j++]);
        G2(3, 4, 9, 14, msg, offset + 2 * s[j++]);
      }
      this.v0l ^= BUF[0] ^ BUF[16];
      this.v0h ^= BUF[1] ^ BUF[17];
      this.v1l ^= BUF[2] ^ BUF[18];
      this.v1h ^= BUF[3] ^ BUF[19];
      this.v2l ^= BUF[4] ^ BUF[20];
      this.v2h ^= BUF[5] ^ BUF[21];
      this.v3l ^= BUF[6] ^ BUF[22];
      this.v3h ^= BUF[7] ^ BUF[23];
      this.v4l ^= BUF[8] ^ BUF[24];
      this.v4h ^= BUF[9] ^ BUF[25];
      this.v5l ^= BUF[10] ^ BUF[26];
      this.v5h ^= BUF[11] ^ BUF[27];
      this.v6l ^= BUF[12] ^ BUF[28];
      this.v6h ^= BUF[13] ^ BUF[29];
      this.v7l ^= BUF[14] ^ BUF[30];
      this.v7h ^= BUF[15] ^ BUF[31];
      BUF.fill(0);
    }
    destroy() {
      this.destroyed = true;
      this.buffer32.fill(0);
      this.set(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    }
  };
  var blake2b = /* @__PURE__ */ wrapConstructorWithOpts((opts) => new BLAKE2b(opts));

  // node_modules/@noble/hashes/esm/blake2s.js
  var IV2 = /* @__PURE__ */ new Uint32Array([1779033703, 3144134277, 1013904242, 2773480762, 1359893119, 2600822924, 528734635, 1541459225]);
  function G12(a, b, c, d, x) {
    a = a + b + x | 0;
    d = rotr(d ^ a, 16);
    c = c + d | 0;
    b = rotr(b ^ c, 12);
    return { a, b, c, d };
  }
  function G22(a, b, c, d, x) {
    a = a + b + x | 0;
    d = rotr(d ^ a, 8);
    c = c + d | 0;
    b = rotr(b ^ c, 7);
    return { a, b, c, d };
  }
  function compress(s, offset, msg, rounds, v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15) {
    let j = 0;
    for (let i = 0; i < rounds; i++) {
      ({ a: v0, b: v4, c: v8, d: v12 } = G12(v0, v4, v8, v12, msg[offset + s[j++]]));
      ({ a: v0, b: v4, c: v8, d: v12 } = G22(v0, v4, v8, v12, msg[offset + s[j++]]));
      ({ a: v1, b: v5, c: v9, d: v13 } = G12(v1, v5, v9, v13, msg[offset + s[j++]]));
      ({ a: v1, b: v5, c: v9, d: v13 } = G22(v1, v5, v9, v13, msg[offset + s[j++]]));
      ({ a: v2, b: v6, c: v10, d: v14 } = G12(v2, v6, v10, v14, msg[offset + s[j++]]));
      ({ a: v2, b: v6, c: v10, d: v14 } = G22(v2, v6, v10, v14, msg[offset + s[j++]]));
      ({ a: v3, b: v7, c: v11, d: v15 } = G12(v3, v7, v11, v15, msg[offset + s[j++]]));
      ({ a: v3, b: v7, c: v11, d: v15 } = G22(v3, v7, v11, v15, msg[offset + s[j++]]));
      ({ a: v0, b: v5, c: v10, d: v15 } = G12(v0, v5, v10, v15, msg[offset + s[j++]]));
      ({ a: v0, b: v5, c: v10, d: v15 } = G22(v0, v5, v10, v15, msg[offset + s[j++]]));
      ({ a: v1, b: v6, c: v11, d: v12 } = G12(v1, v6, v11, v12, msg[offset + s[j++]]));
      ({ a: v1, b: v6, c: v11, d: v12 } = G22(v1, v6, v11, v12, msg[offset + s[j++]]));
      ({ a: v2, b: v7, c: v8, d: v13 } = G12(v2, v7, v8, v13, msg[offset + s[j++]]));
      ({ a: v2, b: v7, c: v8, d: v13 } = G22(v2, v7, v8, v13, msg[offset + s[j++]]));
      ({ a: v3, b: v4, c: v9, d: v14 } = G12(v3, v4, v9, v14, msg[offset + s[j++]]));
      ({ a: v3, b: v4, c: v9, d: v14 } = G22(v3, v4, v9, v14, msg[offset + s[j++]]));
    }
    return { v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15 };
  }
  var BLAKE2s = class extends BLAKE2 {
    constructor(opts = {}) {
      super(64, opts.dkLen === void 0 ? 32 : opts.dkLen, opts, 32, 8, 8);
      this.v0 = IV2[0] | 0;
      this.v1 = IV2[1] | 0;
      this.v2 = IV2[2] | 0;
      this.v3 = IV2[3] | 0;
      this.v4 = IV2[4] | 0;
      this.v5 = IV2[5] | 0;
      this.v6 = IV2[6] | 0;
      this.v7 = IV2[7] | 0;
      const keyLength = opts.key ? opts.key.length : 0;
      this.v0 ^= this.outputLen | keyLength << 8 | 1 << 16 | 1 << 24;
      if (opts.salt) {
        const salt = u32(toBytes(opts.salt));
        this.v4 ^= salt[0];
        this.v5 ^= salt[1];
      }
      if (opts.personalization) {
        const pers = u32(toBytes(opts.personalization));
        this.v6 ^= pers[0];
        this.v7 ^= pers[1];
      }
      if (opts.key) {
        const tmp = new Uint8Array(this.blockLen);
        tmp.set(toBytes(opts.key));
        this.update(tmp);
      }
    }
    get() {
      const { v0, v1, v2, v3, v4, v5, v6, v7 } = this;
      return [v0, v1, v2, v3, v4, v5, v6, v7];
    }
    // prettier-ignore
    set(v0, v1, v2, v3, v4, v5, v6, v7) {
      this.v0 = v0 | 0;
      this.v1 = v1 | 0;
      this.v2 = v2 | 0;
      this.v3 = v3 | 0;
      this.v4 = v4 | 0;
      this.v5 = v5 | 0;
      this.v6 = v6 | 0;
      this.v7 = v7 | 0;
    }
    compress(msg, offset, isLast) {
      const { h, l } = fromBig(BigInt(this.length));
      const { v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15 } = compress(SIGMA, offset, msg, 10, this.v0, this.v1, this.v2, this.v3, this.v4, this.v5, this.v6, this.v7, IV2[0], IV2[1], IV2[2], IV2[3], l ^ IV2[4], h ^ IV2[5], isLast ? ~IV2[6] : IV2[6], IV2[7]);
      this.v0 ^= v0 ^ v8;
      this.v1 ^= v1 ^ v9;
      this.v2 ^= v2 ^ v10;
      this.v3 ^= v3 ^ v11;
      this.v4 ^= v4 ^ v12;
      this.v5 ^= v5 ^ v13;
      this.v6 ^= v6 ^ v14;
      this.v7 ^= v7 ^ v15;
    }
    destroy() {
      this.destroyed = true;
      this.buffer32.fill(0);
      this.set(0, 0, 0, 0, 0, 0, 0, 0);
    }
  };
  var blake2s = /* @__PURE__ */ wrapConstructorWithOpts((opts) => new BLAKE2s(opts));

  // node_modules/@noble/hashes/esm/blake3.js
  var SIGMA2 = /* @__PURE__ */ (() => {
    const Id2 = Array.from({ length: 16 }, (_, i) => i);
    const permute = (arr) => [2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8].map((i) => arr[i]);
    const res = [];
    for (let i = 0, v = Id2; i < 7; i++, v = permute(v))
      res.push(...v);
    return Uint8Array.from(res);
  })();
  var BLAKE3 = class _BLAKE3 extends BLAKE2 {
    constructor(opts = {}, flags = 0) {
      super(64, opts.dkLen === void 0 ? 32 : opts.dkLen, {}, Number.MAX_SAFE_INTEGER, 0, 0);
      this.flags = 0 | 0;
      this.chunkPos = 0;
      this.chunksDone = 0;
      this.stack = [];
      this.posOut = 0;
      this.bufferOut32 = new Uint32Array(16);
      this.chunkOut = 0;
      this.enableXOF = true;
      this.outputLen = opts.dkLen === void 0 ? 32 : opts.dkLen;
      number(this.outputLen);
      if (opts.key !== void 0 && opts.context !== void 0)
        throw new Error("Blake3: only key or context can be specified at same time");
      else if (opts.key !== void 0) {
        const key = toBytes(opts.key).slice();
        if (key.length !== 32)
          throw new Error("Blake3: key should be 32 byte");
        this.IV = u32(key);
        this.flags = flags | 16;
      } else if (opts.context !== void 0) {
        const context_key = new _BLAKE3(
          { dkLen: 32 },
          32
          /* Flags.DERIVE_KEY_CONTEXT */
        ).update(opts.context).digest();
        this.IV = u32(context_key);
        this.flags = flags | 64;
      } else {
        this.IV = IV2.slice();
        this.flags = flags;
      }
      this.state = this.IV.slice();
      this.bufferOut = u8(this.bufferOut32);
    }
    // Unused
    get() {
      return [];
    }
    set() {
    }
    b2Compress(counter, flags, buf, bufPos = 0) {
      const { state: s, pos } = this;
      const { h, l } = fromBig(BigInt(counter), true);
      const { v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15 } = compress(SIGMA2, bufPos, buf, 7, s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], IV2[0], IV2[1], IV2[2], IV2[3], h, l, pos, flags);
      s[0] = v0 ^ v8;
      s[1] = v1 ^ v9;
      s[2] = v2 ^ v10;
      s[3] = v3 ^ v11;
      s[4] = v4 ^ v12;
      s[5] = v5 ^ v13;
      s[6] = v6 ^ v14;
      s[7] = v7 ^ v15;
    }
    compress(buf, bufPos = 0, isLast = false) {
      let flags = this.flags;
      if (!this.chunkPos)
        flags |= 1;
      if (this.chunkPos === 15 || isLast)
        flags |= 2;
      if (!isLast)
        this.pos = this.blockLen;
      this.b2Compress(this.chunksDone, flags, buf, bufPos);
      this.chunkPos += 1;
      if (this.chunkPos === 16 || isLast) {
        let chunk = this.state;
        this.state = this.IV.slice();
        for (let last, chunks = this.chunksDone + 1; isLast || !(chunks & 1); chunks >>= 1) {
          if (!(last = this.stack.pop()))
            break;
          this.buffer32.set(last, 0);
          this.buffer32.set(chunk, 8);
          this.pos = this.blockLen;
          this.b2Compress(0, this.flags | 4, this.buffer32, 0);
          chunk = this.state;
          this.state = this.IV.slice();
        }
        this.chunksDone++;
        this.chunkPos = 0;
        this.stack.push(chunk);
      }
      this.pos = 0;
    }
    _cloneInto(to) {
      to = super._cloneInto(to);
      const { IV: IV5, flags, state, chunkPos, posOut, chunkOut, stack, chunksDone } = this;
      to.state.set(state.slice());
      to.stack = stack.map((i) => Uint32Array.from(i));
      to.IV.set(IV5);
      to.flags = flags;
      to.chunkPos = chunkPos;
      to.chunksDone = chunksDone;
      to.posOut = posOut;
      to.chunkOut = chunkOut;
      to.enableXOF = this.enableXOF;
      to.bufferOut32.set(this.bufferOut32);
      return to;
    }
    destroy() {
      this.destroyed = true;
      this.state.fill(0);
      this.buffer32.fill(0);
      this.IV.fill(0);
      this.bufferOut32.fill(0);
      for (let i of this.stack)
        i.fill(0);
    }
    // Same as b2Compress, but doesn't modify state and returns 16 u32 array (instead of 8)
    b2CompressOut() {
      const { state: s, pos, flags, buffer32, bufferOut32: out32 } = this;
      const { h, l } = fromBig(BigInt(this.chunkOut++));
      const { v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15 } = compress(SIGMA2, 0, buffer32, 7, s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], IV2[0], IV2[1], IV2[2], IV2[3], l, h, pos, flags);
      out32[0] = v0 ^ v8;
      out32[1] = v1 ^ v9;
      out32[2] = v2 ^ v10;
      out32[3] = v3 ^ v11;
      out32[4] = v4 ^ v12;
      out32[5] = v5 ^ v13;
      out32[6] = v6 ^ v14;
      out32[7] = v7 ^ v15;
      out32[8] = s[0] ^ v8;
      out32[9] = s[1] ^ v9;
      out32[10] = s[2] ^ v10;
      out32[11] = s[3] ^ v11;
      out32[12] = s[4] ^ v12;
      out32[13] = s[5] ^ v13;
      out32[14] = s[6] ^ v14;
      out32[15] = s[7] ^ v15;
      this.posOut = 0;
    }
    finish() {
      if (this.finished)
        return;
      this.finished = true;
      this.buffer.fill(0, this.pos);
      let flags = this.flags | 8;
      if (this.stack.length) {
        flags |= 4;
        this.compress(this.buffer32, 0, true);
        this.chunksDone = 0;
        this.pos = this.blockLen;
      } else {
        flags |= (!this.chunkPos ? 1 : 0) | 2;
      }
      this.flags = flags;
      this.b2CompressOut();
    }
    writeInto(out) {
      exists(this, false);
      bytes(out);
      this.finish();
      const { blockLen, bufferOut } = this;
      for (let pos = 0, len = out.length; pos < len; ) {
        if (this.posOut >= blockLen)
          this.b2CompressOut();
        const take = Math.min(blockLen - this.posOut, len - pos);
        out.set(bufferOut.subarray(this.posOut, this.posOut + take), pos);
        this.posOut += take;
        pos += take;
      }
      return out;
    }
    xofInto(out) {
      if (!this.enableXOF)
        throw new Error("XOF is not possible after digest call");
      return this.writeInto(out);
    }
    xof(bytes2) {
      number(bytes2);
      return this.xofInto(new Uint8Array(bytes2));
    }
    digestInto(out) {
      output(out, this);
      if (this.finished)
        throw new Error("digest() was already called");
      this.enableXOF = false;
      this.writeInto(out);
      this.destroy();
      return out;
    }
    digest() {
      return this.digestInto(new Uint8Array(this.outputLen));
    }
  };
  var blake3 = /* @__PURE__ */ wrapXOFConstructorWithOpts((opts) => new BLAKE3(opts));

  // node_modules/@noble/hashes/esm/hmac.js
  var HMAC = class extends Hash {
    constructor(hash2, _key) {
      super();
      this.finished = false;
      this.destroyed = false;
      hash(hash2);
      const key = toBytes(_key);
      this.iHash = hash2.create();
      if (typeof this.iHash.update !== "function")
        throw new Error("Expected instance of class which extends utils.Hash");
      this.blockLen = this.iHash.blockLen;
      this.outputLen = this.iHash.outputLen;
      const blockLen = this.blockLen;
      const pad = new Uint8Array(blockLen);
      pad.set(key.length > blockLen ? hash2.create().update(key).digest() : key);
      for (let i = 0; i < pad.length; i++)
        pad[i] ^= 54;
      this.iHash.update(pad);
      this.oHash = hash2.create();
      for (let i = 0; i < pad.length; i++)
        pad[i] ^= 54 ^ 92;
      this.oHash.update(pad);
      pad.fill(0);
    }
    update(buf) {
      exists(this);
      this.iHash.update(buf);
      return this;
    }
    digestInto(out) {
      exists(this);
      bytes(out, this.outputLen);
      this.finished = true;
      this.iHash.digestInto(out);
      this.oHash.update(out);
      this.oHash.digestInto(out);
      this.destroy();
    }
    digest() {
      const out = new Uint8Array(this.oHash.outputLen);
      this.digestInto(out);
      return out;
    }
    _cloneInto(to) {
      to || (to = Object.create(Object.getPrototypeOf(this), {}));
      const { oHash, iHash, finished, destroyed, blockLen, outputLen } = this;
      to = to;
      to.finished = finished;
      to.destroyed = destroyed;
      to.blockLen = blockLen;
      to.outputLen = outputLen;
      to.oHash = oHash._cloneInto(to.oHash);
      to.iHash = iHash._cloneInto(to.iHash);
      return to;
    }
    destroy() {
      this.destroyed = true;
      this.oHash.destroy();
      this.iHash.destroy();
    }
  };
  var hmac = (hash2, key, message) => new HMAC(hash2, key).update(message).digest();
  hmac.create = (hash2, key) => new HMAC(hash2, key);

  // node_modules/@noble/hashes/esm/hkdf.js
  function extract(hash2, ikm, salt) {
    hash(hash2);
    if (salt === void 0)
      salt = new Uint8Array(hash2.outputLen);
    return hmac(hash2, toBytes(salt), toBytes(ikm));
  }
  var HKDF_COUNTER = /* @__PURE__ */ new Uint8Array([0]);
  var EMPTY_BUFFER = /* @__PURE__ */ new Uint8Array();
  function expand(hash2, prk, info, length = 32) {
    hash(hash2);
    number(length);
    if (length > 255 * hash2.outputLen)
      throw new Error("Length should be <= 255*HashLen");
    const blocks = Math.ceil(length / hash2.outputLen);
    if (info === void 0)
      info = EMPTY_BUFFER;
    const okm = new Uint8Array(blocks * hash2.outputLen);
    const HMAC2 = hmac.create(hash2, prk);
    const HMACTmp = HMAC2._cloneInto();
    const T = new Uint8Array(HMAC2.outputLen);
    for (let counter = 0; counter < blocks; counter++) {
      HKDF_COUNTER[0] = counter + 1;
      HMACTmp.update(counter === 0 ? EMPTY_BUFFER : T).update(info).update(HKDF_COUNTER).digestInto(T);
      okm.set(T, hash2.outputLen * counter);
      HMAC2._cloneInto(HMACTmp);
    }
    HMAC2.destroy();
    HMACTmp.destroy();
    T.fill(0);
    HKDF_COUNTER.fill(0);
    return okm.slice(0, length);
  }
  var hkdf = (hash2, ikm, salt, info, length) => expand(hash2, extract(hash2, ikm, salt), info, length);

  // node_modules/@noble/hashes/esm/pbkdf2.js
  function pbkdf2Init(hash2, _password, _salt, _opts) {
    hash(hash2);
    const opts = checkOpts({ dkLen: 32, asyncTick: 10 }, _opts);
    const { c, dkLen, asyncTick } = opts;
    number(c);
    number(dkLen);
    number(asyncTick);
    if (c < 1)
      throw new Error("PBKDF2: iterations (c) should be >= 1");
    const password = toBytes(_password);
    const salt = toBytes(_salt);
    const DK = new Uint8Array(dkLen);
    const PRF = hmac.create(hash2, password);
    const PRFSalt = PRF._cloneInto().update(salt);
    return { c, dkLen, asyncTick, DK, PRF, PRFSalt };
  }
  function pbkdf2Output(PRF, PRFSalt, DK, prfW, u) {
    PRF.destroy();
    PRFSalt.destroy();
    if (prfW)
      prfW.destroy();
    u.fill(0);
    return DK;
  }
  function pbkdf2(hash2, password, salt, opts) {
    const { c, dkLen, DK, PRF, PRFSalt } = pbkdf2Init(hash2, password, salt, opts);
    let prfW;
    const arr = new Uint8Array(4);
    const view = createView(arr);
    const u = new Uint8Array(PRF.outputLen);
    for (let ti = 1, pos = 0; pos < dkLen; ti++, pos += PRF.outputLen) {
      const Ti = DK.subarray(pos, pos + PRF.outputLen);
      view.setInt32(0, ti, false);
      (prfW = PRFSalt._cloneInto(prfW)).update(arr).digestInto(u);
      Ti.set(u.subarray(0, Ti.length));
      for (let ui = 1; ui < c; ui++) {
        PRF._cloneInto(prfW).update(u).digestInto(u);
        for (let i = 0; i < Ti.length; i++)
          Ti[i] ^= u[i];
      }
    }
    return pbkdf2Output(PRF, PRFSalt, DK, prfW, u);
  }
  async function pbkdf2Async(hash2, password, salt, opts) {
    const { c, dkLen, asyncTick, DK, PRF, PRFSalt } = pbkdf2Init(hash2, password, salt, opts);
    let prfW;
    const arr = new Uint8Array(4);
    const view = createView(arr);
    const u = new Uint8Array(PRF.outputLen);
    for (let ti = 1, pos = 0; pos < dkLen; ti++, pos += PRF.outputLen) {
      const Ti = DK.subarray(pos, pos + PRF.outputLen);
      view.setInt32(0, ti, false);
      (prfW = PRFSalt._cloneInto(prfW)).update(arr).digestInto(u);
      Ti.set(u.subarray(0, Ti.length));
      await asyncLoop(c - 1, asyncTick, () => {
        PRF._cloneInto(prfW).update(u).digestInto(u);
        for (let i = 0; i < Ti.length; i++)
          Ti[i] ^= u[i];
      });
    }
    return pbkdf2Output(PRF, PRFSalt, DK, prfW, u);
  }

  // node_modules/@noble/hashes/esm/_sha2.js
  function setBigUint64(view, byteOffset, value, isLE2) {
    if (typeof view.setBigUint64 === "function")
      return view.setBigUint64(byteOffset, value, isLE2);
    const _32n2 = BigInt(32);
    const _u32_max = BigInt(4294967295);
    const wh = Number(value >> _32n2 & _u32_max);
    const wl = Number(value & _u32_max);
    const h = isLE2 ? 4 : 0;
    const l = isLE2 ? 0 : 4;
    view.setUint32(byteOffset + h, wh, isLE2);
    view.setUint32(byteOffset + l, wl, isLE2);
  }
  var SHA2 = class extends Hash {
    constructor(blockLen, outputLen, padOffset, isLE2) {
      super();
      this.blockLen = blockLen;
      this.outputLen = outputLen;
      this.padOffset = padOffset;
      this.isLE = isLE2;
      this.finished = false;
      this.length = 0;
      this.pos = 0;
      this.destroyed = false;
      this.buffer = new Uint8Array(blockLen);
      this.view = createView(this.buffer);
    }
    update(data) {
      exists(this);
      const { view, buffer, blockLen } = this;
      data = toBytes(data);
      const len = data.length;
      for (let pos = 0; pos < len; ) {
        const take = Math.min(blockLen - this.pos, len - pos);
        if (take === blockLen) {
          const dataView = createView(data);
          for (; blockLen <= len - pos; pos += blockLen)
            this.process(dataView, pos);
          continue;
        }
        buffer.set(data.subarray(pos, pos + take), this.pos);
        this.pos += take;
        pos += take;
        if (this.pos === blockLen) {
          this.process(view, 0);
          this.pos = 0;
        }
      }
      this.length += data.length;
      this.roundClean();
      return this;
    }
    digestInto(out) {
      exists(this);
      output(out, this);
      this.finished = true;
      const { buffer, view, blockLen, isLE: isLE2 } = this;
      let { pos } = this;
      buffer[pos++] = 128;
      this.buffer.subarray(pos).fill(0);
      if (this.padOffset > blockLen - pos) {
        this.process(view, 0);
        pos = 0;
      }
      for (let i = pos; i < blockLen; i++)
        buffer[i] = 0;
      setBigUint64(view, blockLen - 8, BigInt(this.length * 8), isLE2);
      this.process(view, 0);
      const oview = createView(out);
      const len = this.outputLen;
      if (len % 4)
        throw new Error("_sha2: outputLen should be aligned to 32bit");
      const outLen = len / 4;
      const state = this.get();
      if (outLen > state.length)
        throw new Error("_sha2: outputLen bigger than state");
      for (let i = 0; i < outLen; i++)
        oview.setUint32(4 * i, state[i], isLE2);
    }
    digest() {
      const { buffer, outputLen } = this;
      this.digestInto(buffer);
      const res = buffer.slice(0, outputLen);
      this.destroy();
      return res;
    }
    _cloneInto(to) {
      to || (to = new this.constructor());
      to.set(...this.get());
      const { blockLen, buffer, length, finished, destroyed, pos } = this;
      to.length = length;
      to.pos = pos;
      to.finished = finished;
      to.destroyed = destroyed;
      if (length % blockLen)
        to.buffer.set(buffer);
      return to;
    }
  };

  // node_modules/@noble/hashes/esm/ripemd160.js
  var Rho = /* @__PURE__ */ new Uint8Array([7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8]);
  var Id = /* @__PURE__ */ Uint8Array.from({ length: 16 }, (_, i) => i);
  var Pi = /* @__PURE__ */ Id.map((i) => (9 * i + 5) % 16);
  var idxL = [Id];
  var idxR = [Pi];
  for (let i = 0; i < 4; i++)
    for (let j of [idxL, idxR])
      j.push(j[i].map((k) => Rho[k]));
  var shifts = /* @__PURE__ */ [
    [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8],
    [12, 13, 11, 15, 6, 9, 9, 7, 12, 15, 11, 13, 7, 8, 7, 7],
    [13, 15, 14, 11, 7, 7, 6, 8, 13, 14, 13, 12, 5, 5, 6, 9],
    [14, 11, 12, 14, 8, 6, 5, 5, 15, 12, 15, 14, 9, 9, 8, 6],
    [15, 12, 13, 13, 9, 5, 8, 6, 14, 11, 12, 11, 8, 6, 5, 5]
  ].map((i) => new Uint8Array(i));
  var shiftsL = /* @__PURE__ */ idxL.map((idx, i) => idx.map((j) => shifts[i][j]));
  var shiftsR = /* @__PURE__ */ idxR.map((idx, i) => idx.map((j) => shifts[i][j]));
  var Kl = /* @__PURE__ */ new Uint32Array([
    0,
    1518500249,
    1859775393,
    2400959708,
    2840853838
  ]);
  var Kr = /* @__PURE__ */ new Uint32Array([
    1352829926,
    1548603684,
    1836072691,
    2053994217,
    0
  ]);
  var rotl = (word, shift) => word << shift | word >>> 32 - shift;
  function f(group, x, y, z) {
    if (group === 0)
      return x ^ y ^ z;
    else if (group === 1)
      return x & y | ~x & z;
    else if (group === 2)
      return (x | ~y) ^ z;
    else if (group === 3)
      return x & z | y & ~z;
    else
      return x ^ (y | ~z);
  }
  var BUF2 = /* @__PURE__ */ new Uint32Array(16);
  var RIPEMD160 = class extends SHA2 {
    constructor() {
      super(64, 20, 8, true);
      this.h0 = 1732584193 | 0;
      this.h1 = 4023233417 | 0;
      this.h2 = 2562383102 | 0;
      this.h3 = 271733878 | 0;
      this.h4 = 3285377520 | 0;
    }
    get() {
      const { h0, h1, h2, h3, h4 } = this;
      return [h0, h1, h2, h3, h4];
    }
    set(h0, h1, h2, h3, h4) {
      this.h0 = h0 | 0;
      this.h1 = h1 | 0;
      this.h2 = h2 | 0;
      this.h3 = h3 | 0;
      this.h4 = h4 | 0;
    }
    process(view, offset) {
      for (let i = 0; i < 16; i++, offset += 4)
        BUF2[i] = view.getUint32(offset, true);
      let al = this.h0 | 0, ar = al, bl = this.h1 | 0, br = bl, cl = this.h2 | 0, cr = cl, dl = this.h3 | 0, dr = dl, el = this.h4 | 0, er = el;
      for (let group = 0; group < 5; group++) {
        const rGroup = 4 - group;
        const hbl = Kl[group], hbr = Kr[group];
        const rl = idxL[group], rr = idxR[group];
        const sl = shiftsL[group], sr = shiftsR[group];
        for (let i = 0; i < 16; i++) {
          const tl = rotl(al + f(group, bl, cl, dl) + BUF2[rl[i]] + hbl, sl[i]) + el | 0;
          al = el, el = dl, dl = rotl(cl, 10) | 0, cl = bl, bl = tl;
        }
        for (let i = 0; i < 16; i++) {
          const tr = rotl(ar + f(rGroup, br, cr, dr) + BUF2[rr[i]] + hbr, sr[i]) + er | 0;
          ar = er, er = dr, dr = rotl(cr, 10) | 0, cr = br, br = tr;
        }
      }
      this.set(this.h1 + cl + dr | 0, this.h2 + dl + er | 0, this.h3 + el + ar | 0, this.h4 + al + br | 0, this.h0 + bl + cr | 0);
    }
    roundClean() {
      BUF2.fill(0);
    }
    destroy() {
      this.destroyed = true;
      this.buffer.fill(0);
      this.set(0, 0, 0, 0, 0);
    }
  };
  var ripemd160 = /* @__PURE__ */ wrapConstructor(() => new RIPEMD160());

  // node_modules/@noble/hashes/esm/sha256.js
  var Chi = (a, b, c) => a & b ^ ~a & c;
  var Maj = (a, b, c) => a & b ^ a & c ^ b & c;
  var SHA256_K = /* @__PURE__ */ new Uint32Array([
    1116352408,
    1899447441,
    3049323471,
    3921009573,
    961987163,
    1508970993,
    2453635748,
    2870763221,
    3624381080,
    310598401,
    607225278,
    1426881987,
    1925078388,
    2162078206,
    2614888103,
    3248222580,
    3835390401,
    4022224774,
    264347078,
    604807628,
    770255983,
    1249150122,
    1555081692,
    1996064986,
    2554220882,
    2821834349,
    2952996808,
    3210313671,
    3336571891,
    3584528711,
    113926993,
    338241895,
    666307205,
    773529912,
    1294757372,
    1396182291,
    1695183700,
    1986661051,
    2177026350,
    2456956037,
    2730485921,
    2820302411,
    3259730800,
    3345764771,
    3516065817,
    3600352804,
    4094571909,
    275423344,
    430227734,
    506948616,
    659060556,
    883997877,
    958139571,
    1322822218,
    1537002063,
    1747873779,
    1955562222,
    2024104815,
    2227730452,
    2361852424,
    2428436474,
    2756734187,
    3204031479,
    3329325298
  ]);
  var IV3 = /* @__PURE__ */ new Uint32Array([
    1779033703,
    3144134277,
    1013904242,
    2773480762,
    1359893119,
    2600822924,
    528734635,
    1541459225
  ]);
  var SHA256_W = /* @__PURE__ */ new Uint32Array(64);
  var SHA256 = class extends SHA2 {
    constructor() {
      super(64, 32, 8, false);
      this.A = IV3[0] | 0;
      this.B = IV3[1] | 0;
      this.C = IV3[2] | 0;
      this.D = IV3[3] | 0;
      this.E = IV3[4] | 0;
      this.F = IV3[5] | 0;
      this.G = IV3[6] | 0;
      this.H = IV3[7] | 0;
    }
    get() {
      const { A, B, C, D, E, F, G: G3, H } = this;
      return [A, B, C, D, E, F, G3, H];
    }
    // prettier-ignore
    set(A, B, C, D, E, F, G3, H) {
      this.A = A | 0;
      this.B = B | 0;
      this.C = C | 0;
      this.D = D | 0;
      this.E = E | 0;
      this.F = F | 0;
      this.G = G3 | 0;
      this.H = H | 0;
    }
    process(view, offset) {
      for (let i = 0; i < 16; i++, offset += 4)
        SHA256_W[i] = view.getUint32(offset, false);
      for (let i = 16; i < 64; i++) {
        const W15 = SHA256_W[i - 15];
        const W2 = SHA256_W[i - 2];
        const s0 = rotr(W15, 7) ^ rotr(W15, 18) ^ W15 >>> 3;
        const s1 = rotr(W2, 17) ^ rotr(W2, 19) ^ W2 >>> 10;
        SHA256_W[i] = s1 + SHA256_W[i - 7] + s0 + SHA256_W[i - 16] | 0;
      }
      let { A, B, C, D, E, F, G: G3, H } = this;
      for (let i = 0; i < 64; i++) {
        const sigma1 = rotr(E, 6) ^ rotr(E, 11) ^ rotr(E, 25);
        const T1 = H + sigma1 + Chi(E, F, G3) + SHA256_K[i] + SHA256_W[i] | 0;
        const sigma0 = rotr(A, 2) ^ rotr(A, 13) ^ rotr(A, 22);
        const T2 = sigma0 + Maj(A, B, C) | 0;
        H = G3;
        G3 = F;
        F = E;
        E = D + T1 | 0;
        D = C;
        C = B;
        B = A;
        A = T1 + T2 | 0;
      }
      A = A + this.A | 0;
      B = B + this.B | 0;
      C = C + this.C | 0;
      D = D + this.D | 0;
      E = E + this.E | 0;
      F = F + this.F | 0;
      G3 = G3 + this.G | 0;
      H = H + this.H | 0;
      this.set(A, B, C, D, E, F, G3, H);
    }
    roundClean() {
      SHA256_W.fill(0);
    }
    destroy() {
      this.set(0, 0, 0, 0, 0, 0, 0, 0);
      this.buffer.fill(0);
    }
  };
  var sha256 = /* @__PURE__ */ wrapConstructor(() => new SHA256());

  // node_modules/@noble/hashes/esm/scrypt.js
  var rotl2 = (a, b) => a << b | a >>> 32 - b;
  function XorAndSalsa(prev, pi, input, ii, out, oi) {
    let y00 = prev[pi++] ^ input[ii++], y01 = prev[pi++] ^ input[ii++];
    let y02 = prev[pi++] ^ input[ii++], y03 = prev[pi++] ^ input[ii++];
    let y04 = prev[pi++] ^ input[ii++], y05 = prev[pi++] ^ input[ii++];
    let y06 = prev[pi++] ^ input[ii++], y07 = prev[pi++] ^ input[ii++];
    let y08 = prev[pi++] ^ input[ii++], y09 = prev[pi++] ^ input[ii++];
    let y10 = prev[pi++] ^ input[ii++], y11 = prev[pi++] ^ input[ii++];
    let y12 = prev[pi++] ^ input[ii++], y13 = prev[pi++] ^ input[ii++];
    let y14 = prev[pi++] ^ input[ii++], y15 = prev[pi++] ^ input[ii++];
    let x00 = y00, x01 = y01, x02 = y02, x03 = y03, x04 = y04, x05 = y05, x06 = y06, x07 = y07, x08 = y08, x09 = y09, x10 = y10, x11 = y11, x12 = y12, x13 = y13, x14 = y14, x15 = y15;
    for (let i = 0; i < 8; i += 2) {
      x04 ^= rotl2(x00 + x12 | 0, 7);
      x08 ^= rotl2(x04 + x00 | 0, 9);
      x12 ^= rotl2(x08 + x04 | 0, 13);
      x00 ^= rotl2(x12 + x08 | 0, 18);
      x09 ^= rotl2(x05 + x01 | 0, 7);
      x13 ^= rotl2(x09 + x05 | 0, 9);
      x01 ^= rotl2(x13 + x09 | 0, 13);
      x05 ^= rotl2(x01 + x13 | 0, 18);
      x14 ^= rotl2(x10 + x06 | 0, 7);
      x02 ^= rotl2(x14 + x10 | 0, 9);
      x06 ^= rotl2(x02 + x14 | 0, 13);
      x10 ^= rotl2(x06 + x02 | 0, 18);
      x03 ^= rotl2(x15 + x11 | 0, 7);
      x07 ^= rotl2(x03 + x15 | 0, 9);
      x11 ^= rotl2(x07 + x03 | 0, 13);
      x15 ^= rotl2(x11 + x07 | 0, 18);
      x01 ^= rotl2(x00 + x03 | 0, 7);
      x02 ^= rotl2(x01 + x00 | 0, 9);
      x03 ^= rotl2(x02 + x01 | 0, 13);
      x00 ^= rotl2(x03 + x02 | 0, 18);
      x06 ^= rotl2(x05 + x04 | 0, 7);
      x07 ^= rotl2(x06 + x05 | 0, 9);
      x04 ^= rotl2(x07 + x06 | 0, 13);
      x05 ^= rotl2(x04 + x07 | 0, 18);
      x11 ^= rotl2(x10 + x09 | 0, 7);
      x08 ^= rotl2(x11 + x10 | 0, 9);
      x09 ^= rotl2(x08 + x11 | 0, 13);
      x10 ^= rotl2(x09 + x08 | 0, 18);
      x12 ^= rotl2(x15 + x14 | 0, 7);
      x13 ^= rotl2(x12 + x15 | 0, 9);
      x14 ^= rotl2(x13 + x12 | 0, 13);
      x15 ^= rotl2(x14 + x13 | 0, 18);
    }
    out[oi++] = y00 + x00 | 0;
    out[oi++] = y01 + x01 | 0;
    out[oi++] = y02 + x02 | 0;
    out[oi++] = y03 + x03 | 0;
    out[oi++] = y04 + x04 | 0;
    out[oi++] = y05 + x05 | 0;
    out[oi++] = y06 + x06 | 0;
    out[oi++] = y07 + x07 | 0;
    out[oi++] = y08 + x08 | 0;
    out[oi++] = y09 + x09 | 0;
    out[oi++] = y10 + x10 | 0;
    out[oi++] = y11 + x11 | 0;
    out[oi++] = y12 + x12 | 0;
    out[oi++] = y13 + x13 | 0;
    out[oi++] = y14 + x14 | 0;
    out[oi++] = y15 + x15 | 0;
  }
  function BlockMix(input, ii, out, oi, r) {
    let head = oi + 0;
    let tail = oi + 16 * r;
    for (let i = 0; i < 16; i++)
      out[tail + i] = input[ii + (2 * r - 1) * 16 + i];
    for (let i = 0; i < r; i++, head += 16, ii += 16) {
      XorAndSalsa(out, tail, input, ii, out, head);
      if (i > 0)
        tail += 16;
      XorAndSalsa(out, head, input, ii += 16, out, tail);
    }
  }
  function scryptInit(password, salt, _opts) {
    const opts = checkOpts({
      dkLen: 32,
      asyncTick: 10,
      maxmem: 1024 ** 3 + 1024
    }, _opts);
    const { N, r, p, dkLen, asyncTick, maxmem, onProgress } = opts;
    number(N);
    number(r);
    number(p);
    number(dkLen);
    number(asyncTick);
    number(maxmem);
    if (onProgress !== void 0 && typeof onProgress !== "function")
      throw new Error("progressCb should be function");
    const blockSize = 128 * r;
    const blockSize32 = blockSize / 4;
    if (N <= 1 || (N & N - 1) !== 0 || N >= 2 ** (blockSize / 8) || N > 2 ** 32) {
      throw new Error("Scrypt: N must be larger than 1, a power of 2, less than 2^(128 * r / 8) and less than 2^32");
    }
    if (p < 0 || p > (2 ** 32 - 1) * 32 / blockSize) {
      throw new Error("Scrypt: p must be a positive integer less than or equal to ((2^32 - 1) * 32) / (128 * r)");
    }
    if (dkLen < 0 || dkLen > (2 ** 32 - 1) * 32) {
      throw new Error("Scrypt: dkLen should be positive integer less than or equal to (2^32 - 1) * 32");
    }
    const memUsed = blockSize * (N + p);
    if (memUsed > maxmem) {
      throw new Error(`Scrypt: parameters too large, ${memUsed} (128 * r * (N + p)) > ${maxmem} (maxmem)`);
    }
    const B = pbkdf2(sha256, password, salt, { c: 1, dkLen: blockSize * p });
    const B32 = u32(B);
    const V = u32(new Uint8Array(blockSize * N));
    const tmp = u32(new Uint8Array(blockSize));
    let blockMixCb = () => {
    };
    if (onProgress) {
      const totalBlockMix = 2 * N * p;
      const callbackPer = Math.max(Math.floor(totalBlockMix / 1e4), 1);
      let blockMixCnt = 0;
      blockMixCb = () => {
        blockMixCnt++;
        if (onProgress && (!(blockMixCnt % callbackPer) || blockMixCnt === totalBlockMix))
          onProgress(blockMixCnt / totalBlockMix);
      };
    }
    return { N, r, p, dkLen, blockSize32, V, B32, B, tmp, blockMixCb, asyncTick };
  }
  function scryptOutput(password, dkLen, B, V, tmp) {
    const res = pbkdf2(sha256, password, B, { c: 1, dkLen });
    B.fill(0);
    V.fill(0);
    tmp.fill(0);
    return res;
  }
  function scrypt(password, salt, opts) {
    const { N, r, p, dkLen, blockSize32, V, B32, B, tmp, blockMixCb } = scryptInit(password, salt, opts);
    for (let pi = 0; pi < p; pi++) {
      const Pi2 = blockSize32 * pi;
      for (let i = 0; i < blockSize32; i++)
        V[i] = B32[Pi2 + i];
      for (let i = 0, pos = 0; i < N - 1; i++) {
        BlockMix(V, pos, V, pos += blockSize32, r);
        blockMixCb();
      }
      BlockMix(V, (N - 1) * blockSize32, B32, Pi2, r);
      blockMixCb();
      for (let i = 0; i < N; i++) {
        const j = B32[Pi2 + blockSize32 - 16] % N;
        for (let k = 0; k < blockSize32; k++)
          tmp[k] = B32[Pi2 + k] ^ V[j * blockSize32 + k];
        BlockMix(tmp, 0, B32, Pi2, r);
        blockMixCb();
      }
    }
    return scryptOutput(password, dkLen, B, V, tmp);
  }
  async function scryptAsync(password, salt, opts) {
    const { N, r, p, dkLen, blockSize32, V, B32, B, tmp, blockMixCb, asyncTick } = scryptInit(password, salt, opts);
    for (let pi = 0; pi < p; pi++) {
      const Pi2 = blockSize32 * pi;
      for (let i = 0; i < blockSize32; i++)
        V[i] = B32[Pi2 + i];
      let pos = 0;
      await asyncLoop(N - 1, asyncTick, () => {
        BlockMix(V, pos, V, pos += blockSize32, r);
        blockMixCb();
      });
      BlockMix(V, (N - 1) * blockSize32, B32, Pi2, r);
      blockMixCb();
      await asyncLoop(N, asyncTick, () => {
        const j = B32[Pi2 + blockSize32 - 16] % N;
        for (let k = 0; k < blockSize32; k++)
          tmp[k] = B32[Pi2 + k] ^ V[j * blockSize32 + k];
        BlockMix(tmp, 0, B32, Pi2, r);
        blockMixCb();
      });
    }
    return scryptOutput(password, dkLen, B, V, tmp);
  }

  // node_modules/@noble/hashes/esm/sha512.js
  var [SHA512_Kh, SHA512_Kl] = /* @__PURE__ */ (() => u64_default.split([
    "0x428a2f98d728ae22",
    "0x7137449123ef65cd",
    "0xb5c0fbcfec4d3b2f",
    "0xe9b5dba58189dbbc",
    "0x3956c25bf348b538",
    "0x59f111f1b605d019",
    "0x923f82a4af194f9b",
    "0xab1c5ed5da6d8118",
    "0xd807aa98a3030242",
    "0x12835b0145706fbe",
    "0x243185be4ee4b28c",
    "0x550c7dc3d5ffb4e2",
    "0x72be5d74f27b896f",
    "0x80deb1fe3b1696b1",
    "0x9bdc06a725c71235",
    "0xc19bf174cf692694",
    "0xe49b69c19ef14ad2",
    "0xefbe4786384f25e3",
    "0x0fc19dc68b8cd5b5",
    "0x240ca1cc77ac9c65",
    "0x2de92c6f592b0275",
    "0x4a7484aa6ea6e483",
    "0x5cb0a9dcbd41fbd4",
    "0x76f988da831153b5",
    "0x983e5152ee66dfab",
    "0xa831c66d2db43210",
    "0xb00327c898fb213f",
    "0xbf597fc7beef0ee4",
    "0xc6e00bf33da88fc2",
    "0xd5a79147930aa725",
    "0x06ca6351e003826f",
    "0x142929670a0e6e70",
    "0x27b70a8546d22ffc",
    "0x2e1b21385c26c926",
    "0x4d2c6dfc5ac42aed",
    "0x53380d139d95b3df",
    "0x650a73548baf63de",
    "0x766a0abb3c77b2a8",
    "0x81c2c92e47edaee6",
    "0x92722c851482353b",
    "0xa2bfe8a14cf10364",
    "0xa81a664bbc423001",
    "0xc24b8b70d0f89791",
    "0xc76c51a30654be30",
    "0xd192e819d6ef5218",
    "0xd69906245565a910",
    "0xf40e35855771202a",
    "0x106aa07032bbd1b8",
    "0x19a4c116b8d2d0c8",
    "0x1e376c085141ab53",
    "0x2748774cdf8eeb99",
    "0x34b0bcb5e19b48a8",
    "0x391c0cb3c5c95a63",
    "0x4ed8aa4ae3418acb",
    "0x5b9cca4f7763e373",
    "0x682e6ff3d6b2b8a3",
    "0x748f82ee5defb2fc",
    "0x78a5636f43172f60",
    "0x84c87814a1f0ab72",
    "0x8cc702081a6439ec",
    "0x90befffa23631e28",
    "0xa4506cebde82bde9",
    "0xbef9a3f7b2c67915",
    "0xc67178f2e372532b",
    "0xca273eceea26619c",
    "0xd186b8c721c0c207",
    "0xeada7dd6cde0eb1e",
    "0xf57d4f7fee6ed178",
    "0x06f067aa72176fba",
    "0x0a637dc5a2c898a6",
    "0x113f9804bef90dae",
    "0x1b710b35131c471b",
    "0x28db77f523047d84",
    "0x32caab7b40c72493",
    "0x3c9ebe0a15c9bebc",
    "0x431d67c49c100d4c",
    "0x4cc5d4becb3e42b6",
    "0x597f299cfc657e2a",
    "0x5fcb6fab3ad6faec",
    "0x6c44198c4a475817"
  ].map((n) => BigInt(n))))();
  var SHA512_W_H = /* @__PURE__ */ new Uint32Array(80);
  var SHA512_W_L = /* @__PURE__ */ new Uint32Array(80);
  var SHA512 = class extends SHA2 {
    constructor() {
      super(128, 64, 16, false);
      this.Ah = 1779033703 | 0;
      this.Al = 4089235720 | 0;
      this.Bh = 3144134277 | 0;
      this.Bl = 2227873595 | 0;
      this.Ch = 1013904242 | 0;
      this.Cl = 4271175723 | 0;
      this.Dh = 2773480762 | 0;
      this.Dl = 1595750129 | 0;
      this.Eh = 1359893119 | 0;
      this.El = 2917565137 | 0;
      this.Fh = 2600822924 | 0;
      this.Fl = 725511199 | 0;
      this.Gh = 528734635 | 0;
      this.Gl = 4215389547 | 0;
      this.Hh = 1541459225 | 0;
      this.Hl = 327033209 | 0;
    }
    // prettier-ignore
    get() {
      const { Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl } = this;
      return [Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl];
    }
    // prettier-ignore
    set(Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl) {
      this.Ah = Ah | 0;
      this.Al = Al | 0;
      this.Bh = Bh | 0;
      this.Bl = Bl | 0;
      this.Ch = Ch | 0;
      this.Cl = Cl | 0;
      this.Dh = Dh | 0;
      this.Dl = Dl | 0;
      this.Eh = Eh | 0;
      this.El = El | 0;
      this.Fh = Fh | 0;
      this.Fl = Fl | 0;
      this.Gh = Gh | 0;
      this.Gl = Gl | 0;
      this.Hh = Hh | 0;
      this.Hl = Hl | 0;
    }
    process(view, offset) {
      for (let i = 0; i < 16; i++, offset += 4) {
        SHA512_W_H[i] = view.getUint32(offset);
        SHA512_W_L[i] = view.getUint32(offset += 4);
      }
      for (let i = 16; i < 80; i++) {
        const W15h = SHA512_W_H[i - 15] | 0;
        const W15l = SHA512_W_L[i - 15] | 0;
        const s0h = u64_default.rotrSH(W15h, W15l, 1) ^ u64_default.rotrSH(W15h, W15l, 8) ^ u64_default.shrSH(W15h, W15l, 7);
        const s0l = u64_default.rotrSL(W15h, W15l, 1) ^ u64_default.rotrSL(W15h, W15l, 8) ^ u64_default.shrSL(W15h, W15l, 7);
        const W2h = SHA512_W_H[i - 2] | 0;
        const W2l = SHA512_W_L[i - 2] | 0;
        const s1h = u64_default.rotrSH(W2h, W2l, 19) ^ u64_default.rotrBH(W2h, W2l, 61) ^ u64_default.shrSH(W2h, W2l, 6);
        const s1l = u64_default.rotrSL(W2h, W2l, 19) ^ u64_default.rotrBL(W2h, W2l, 61) ^ u64_default.shrSL(W2h, W2l, 6);
        const SUMl = u64_default.add4L(s0l, s1l, SHA512_W_L[i - 7], SHA512_W_L[i - 16]);
        const SUMh = u64_default.add4H(SUMl, s0h, s1h, SHA512_W_H[i - 7], SHA512_W_H[i - 16]);
        SHA512_W_H[i] = SUMh | 0;
        SHA512_W_L[i] = SUMl | 0;
      }
      let { Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl } = this;
      for (let i = 0; i < 80; i++) {
        const sigma1h = u64_default.rotrSH(Eh, El, 14) ^ u64_default.rotrSH(Eh, El, 18) ^ u64_default.rotrBH(Eh, El, 41);
        const sigma1l = u64_default.rotrSL(Eh, El, 14) ^ u64_default.rotrSL(Eh, El, 18) ^ u64_default.rotrBL(Eh, El, 41);
        const CHIh = Eh & Fh ^ ~Eh & Gh;
        const CHIl = El & Fl ^ ~El & Gl;
        const T1ll = u64_default.add5L(Hl, sigma1l, CHIl, SHA512_Kl[i], SHA512_W_L[i]);
        const T1h = u64_default.add5H(T1ll, Hh, sigma1h, CHIh, SHA512_Kh[i], SHA512_W_H[i]);
        const T1l = T1ll | 0;
        const sigma0h = u64_default.rotrSH(Ah, Al, 28) ^ u64_default.rotrBH(Ah, Al, 34) ^ u64_default.rotrBH(Ah, Al, 39);
        const sigma0l = u64_default.rotrSL(Ah, Al, 28) ^ u64_default.rotrBL(Ah, Al, 34) ^ u64_default.rotrBL(Ah, Al, 39);
        const MAJh = Ah & Bh ^ Ah & Ch ^ Bh & Ch;
        const MAJl = Al & Bl ^ Al & Cl ^ Bl & Cl;
        Hh = Gh | 0;
        Hl = Gl | 0;
        Gh = Fh | 0;
        Gl = Fl | 0;
        Fh = Eh | 0;
        Fl = El | 0;
        ({ h: Eh, l: El } = u64_default.add(Dh | 0, Dl | 0, T1h | 0, T1l | 0));
        Dh = Ch | 0;
        Dl = Cl | 0;
        Ch = Bh | 0;
        Cl = Bl | 0;
        Bh = Ah | 0;
        Bl = Al | 0;
        const All = u64_default.add3L(T1l, sigma0l, MAJl);
        Ah = u64_default.add3H(All, T1h, sigma0h, MAJh);
        Al = All | 0;
      }
      ({ h: Ah, l: Al } = u64_default.add(this.Ah | 0, this.Al | 0, Ah | 0, Al | 0));
      ({ h: Bh, l: Bl } = u64_default.add(this.Bh | 0, this.Bl | 0, Bh | 0, Bl | 0));
      ({ h: Ch, l: Cl } = u64_default.add(this.Ch | 0, this.Cl | 0, Ch | 0, Cl | 0));
      ({ h: Dh, l: Dl } = u64_default.add(this.Dh | 0, this.Dl | 0, Dh | 0, Dl | 0));
      ({ h: Eh, l: El } = u64_default.add(this.Eh | 0, this.El | 0, Eh | 0, El | 0));
      ({ h: Fh, l: Fl } = u64_default.add(this.Fh | 0, this.Fl | 0, Fh | 0, Fl | 0));
      ({ h: Gh, l: Gl } = u64_default.add(this.Gh | 0, this.Gl | 0, Gh | 0, Gl | 0));
      ({ h: Hh, l: Hl } = u64_default.add(this.Hh | 0, this.Hl | 0, Hh | 0, Hl | 0));
      this.set(Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl);
    }
    roundClean() {
      SHA512_W_H.fill(0);
      SHA512_W_L.fill(0);
    }
    destroy() {
      this.buffer.fill(0);
      this.set(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    }
  };
  var sha512 = /* @__PURE__ */ wrapConstructor(() => new SHA512());

  // node_modules/@noble/hashes/esm/sha3.js
  var [SHA3_PI, SHA3_ROTL, _SHA3_IOTA] = [[], [], []];
  var _0n = /* @__PURE__ */ BigInt(0);
  var _1n = /* @__PURE__ */ BigInt(1);
  var _2n = /* @__PURE__ */ BigInt(2);
  var _7n = /* @__PURE__ */ BigInt(7);
  var _256n = /* @__PURE__ */ BigInt(256);
  var _0x71n = /* @__PURE__ */ BigInt(113);
  for (let round = 0, R = _1n, x = 1, y = 0; round < 24; round++) {
    [x, y] = [y, (2 * x + 3 * y) % 5];
    SHA3_PI.push(2 * (5 * y + x));
    SHA3_ROTL.push((round + 1) * (round + 2) / 2 % 64);
    let t = _0n;
    for (let j = 0; j < 7; j++) {
      R = (R << _1n ^ (R >> _7n) * _0x71n) % _256n;
      if (R & _2n)
        t ^= _1n << (_1n << /* @__PURE__ */ BigInt(j)) - _1n;
    }
    _SHA3_IOTA.push(t);
  }
  var [SHA3_IOTA_H, SHA3_IOTA_L] = /* @__PURE__ */ split(_SHA3_IOTA, true);
  var rotlH = (h, l, s) => s > 32 ? rotlBH(h, l, s) : rotlSH(h, l, s);
  var rotlL = (h, l, s) => s > 32 ? rotlBL(h, l, s) : rotlSL(h, l, s);
  function keccakP(s, rounds = 24) {
    const B = new Uint32Array(5 * 2);
    for (let round = 24 - rounds; round < 24; round++) {
      for (let x = 0; x < 10; x++)
        B[x] = s[x] ^ s[x + 10] ^ s[x + 20] ^ s[x + 30] ^ s[x + 40];
      for (let x = 0; x < 10; x += 2) {
        const idx1 = (x + 8) % 10;
        const idx0 = (x + 2) % 10;
        const B0 = B[idx0];
        const B1 = B[idx0 + 1];
        const Th = rotlH(B0, B1, 1) ^ B[idx1];
        const Tl = rotlL(B0, B1, 1) ^ B[idx1 + 1];
        for (let y = 0; y < 50; y += 10) {
          s[x + y] ^= Th;
          s[x + y + 1] ^= Tl;
        }
      }
      let curH = s[2];
      let curL = s[3];
      for (let t = 0; t < 24; t++) {
        const shift = SHA3_ROTL[t];
        const Th = rotlH(curH, curL, shift);
        const Tl = rotlL(curH, curL, shift);
        const PI = SHA3_PI[t];
        curH = s[PI];
        curL = s[PI + 1];
        s[PI] = Th;
        s[PI + 1] = Tl;
      }
      for (let y = 0; y < 50; y += 10) {
        for (let x = 0; x < 10; x++)
          B[x] = s[y + x];
        for (let x = 0; x < 10; x++)
          s[y + x] ^= ~B[(x + 2) % 10] & B[(x + 4) % 10];
      }
      s[0] ^= SHA3_IOTA_H[round];
      s[1] ^= SHA3_IOTA_L[round];
    }
    B.fill(0);
  }
  var Keccak = class _Keccak extends Hash {
    // NOTE: we accept arguments in bytes instead of bits here.
    constructor(blockLen, suffix, outputLen, enableXOF = false, rounds = 24) {
      super();
      this.blockLen = blockLen;
      this.suffix = suffix;
      this.outputLen = outputLen;
      this.enableXOF = enableXOF;
      this.rounds = rounds;
      this.pos = 0;
      this.posOut = 0;
      this.finished = false;
      this.destroyed = false;
      number(outputLen);
      if (0 >= this.blockLen || this.blockLen >= 200)
        throw new Error("Sha3 supports only keccak-f1600 function");
      this.state = new Uint8Array(200);
      this.state32 = u32(this.state);
    }
    keccak() {
      keccakP(this.state32, this.rounds);
      this.posOut = 0;
      this.pos = 0;
    }
    update(data) {
      exists(this);
      const { blockLen, state } = this;
      data = toBytes(data);
      const len = data.length;
      for (let pos = 0; pos < len; ) {
        const take = Math.min(blockLen - this.pos, len - pos);
        for (let i = 0; i < take; i++)
          state[this.pos++] ^= data[pos++];
        if (this.pos === blockLen)
          this.keccak();
      }
      return this;
    }
    finish() {
      if (this.finished)
        return;
      this.finished = true;
      const { state, suffix, pos, blockLen } = this;
      state[pos] ^= suffix;
      if ((suffix & 128) !== 0 && pos === blockLen - 1)
        this.keccak();
      state[blockLen - 1] ^= 128;
      this.keccak();
    }
    writeInto(out) {
      exists(this, false);
      bytes(out);
      this.finish();
      const bufferOut = this.state;
      const { blockLen } = this;
      for (let pos = 0, len = out.length; pos < len; ) {
        if (this.posOut >= blockLen)
          this.keccak();
        const take = Math.min(blockLen - this.posOut, len - pos);
        out.set(bufferOut.subarray(this.posOut, this.posOut + take), pos);
        this.posOut += take;
        pos += take;
      }
      return out;
    }
    xofInto(out) {
      if (!this.enableXOF)
        throw new Error("XOF is not possible for this instance");
      return this.writeInto(out);
    }
    xof(bytes2) {
      number(bytes2);
      return this.xofInto(new Uint8Array(bytes2));
    }
    digestInto(out) {
      output(out, this);
      if (this.finished)
        throw new Error("digest() was already called");
      this.writeInto(out);
      this.destroy();
      return out;
    }
    digest() {
      return this.digestInto(new Uint8Array(this.outputLen));
    }
    destroy() {
      this.destroyed = true;
      this.state.fill(0);
    }
    _cloneInto(to) {
      const { blockLen, suffix, outputLen, rounds, enableXOF } = this;
      to || (to = new _Keccak(blockLen, suffix, outputLen, enableXOF, rounds));
      to.state32.set(this.state32);
      to.pos = this.pos;
      to.posOut = this.posOut;
      to.finished = this.finished;
      to.rounds = rounds;
      to.suffix = suffix;
      to.outputLen = outputLen;
      to.enableXOF = enableXOF;
      to.destroyed = this.destroyed;
      return to;
    }
  };
  var gen = (suffix, blockLen, outputLen) => wrapConstructor(() => new Keccak(blockLen, suffix, outputLen));
  var sha3_224 = /* @__PURE__ */ gen(6, 144, 224 / 8);
  var sha3_256 = /* @__PURE__ */ gen(6, 136, 256 / 8);
  var sha3_384 = /* @__PURE__ */ gen(6, 104, 384 / 8);
  var sha3_512 = /* @__PURE__ */ gen(6, 72, 512 / 8);
  var keccak_224 = /* @__PURE__ */ gen(1, 144, 224 / 8);
  var keccak_256 = /* @__PURE__ */ gen(1, 136, 256 / 8);
  var keccak_384 = /* @__PURE__ */ gen(1, 104, 384 / 8);
  var keccak_512 = /* @__PURE__ */ gen(1, 72, 512 / 8);
  var genShake = (suffix, blockLen, outputLen) => wrapXOFConstructorWithOpts((opts = {}) => new Keccak(blockLen, suffix, opts.dkLen === void 0 ? outputLen : opts.dkLen, true));
  var shake128 = /* @__PURE__ */ genShake(31, 168, 128 / 8);
  var shake256 = /* @__PURE__ */ genShake(31, 136, 256 / 8);

  // node_modules/@noble/hashes/esm/sha3-addons.js
  function leftEncode(n) {
    const res = [n & 255];
    n >>= 8;
    for (; n > 0; n >>= 8)
      res.unshift(n & 255);
    res.unshift(res.length);
    return new Uint8Array(res);
  }
  function rightEncode(n) {
    const res = [n & 255];
    n >>= 8;
    for (; n > 0; n >>= 8)
      res.unshift(n & 255);
    res.push(res.length);
    return new Uint8Array(res);
  }
  function chooseLen(opts, outputLen) {
    return opts.dkLen === void 0 ? outputLen : opts.dkLen;
  }
  var toBytesOptional = (buf) => buf !== void 0 ? toBytes(buf) : new Uint8Array([]);
  var getPadding = (len, block2) => new Uint8Array((block2 - len % block2) % block2);
  function cshakePers(hash2, opts = {}) {
    if (!opts || !opts.personalization && !opts.NISTfn)
      return hash2;
    const blockLenBytes = leftEncode(hash2.blockLen);
    const fn = toBytesOptional(opts.NISTfn);
    const fnLen = leftEncode(8 * fn.length);
    const pers = toBytesOptional(opts.personalization);
    const persLen = leftEncode(8 * pers.length);
    if (!fn.length && !pers.length)
      return hash2;
    hash2.suffix = 4;
    hash2.update(blockLenBytes).update(fnLen).update(fn).update(persLen).update(pers);
    let totalLen = blockLenBytes.length + fnLen.length + fn.length + persLen.length + pers.length;
    hash2.update(getPadding(totalLen, hash2.blockLen));
    return hash2;
  }
  var gencShake = (suffix, blockLen, outputLen) => wrapConstructorWithOpts((opts = {}) => cshakePers(new Keccak(blockLen, suffix, chooseLen(opts, outputLen), true), opts));
  var cshake128 = /* @__PURE__ */ (() => gencShake(31, 168, 128 / 8))();
  var cshake256 = /* @__PURE__ */ (() => gencShake(31, 136, 256 / 8))();
  var KMAC = class extends Keccak {
    constructor(blockLen, outputLen, enableXOF, key, opts = {}) {
      super(blockLen, 31, outputLen, enableXOF);
      cshakePers(this, { NISTfn: "KMAC", personalization: opts.personalization });
      key = toBytes(key);
      const blockLenBytes = leftEncode(this.blockLen);
      const keyLen = leftEncode(8 * key.length);
      this.update(blockLenBytes).update(keyLen).update(key);
      const totalLen = blockLenBytes.length + keyLen.length + key.length;
      this.update(getPadding(totalLen, this.blockLen));
    }
    finish() {
      if (!this.finished)
        this.update(rightEncode(this.enableXOF ? 0 : this.outputLen * 8));
      super.finish();
    }
    _cloneInto(to) {
      if (!to) {
        to = Object.create(Object.getPrototypeOf(this), {});
        to.state = this.state.slice();
        to.blockLen = this.blockLen;
        to.state32 = u32(to.state);
      }
      return super._cloneInto(to);
    }
    clone() {
      return this._cloneInto();
    }
  };
  function genKmac(blockLen, outputLen, xof = false) {
    const kmac = (key, message, opts) => kmac.create(key, opts).update(message).digest();
    kmac.create = (key, opts = {}) => new KMAC(blockLen, chooseLen(opts, outputLen), xof, key, opts);
    return kmac;
  }
  var kmac128 = /* @__PURE__ */ (() => genKmac(168, 128 / 8))();
  var kmac256 = /* @__PURE__ */ (() => genKmac(136, 256 / 8))();
  var genTurboshake = (blockLen, outputLen) => wrapXOFConstructorWithOpts((opts = {}) => {
    const D = opts.D === void 0 ? 31 : opts.D;
    if (!Number.isSafeInteger(D) || D < 1 || D > 127)
      throw new Error(`turboshake: wrong domain separation byte: ${D}, should be 0x01..0x7f`);
    return new Keccak(blockLen, D, opts.dkLen === void 0 ? outputLen : opts.dkLen, true, 12);
  });
  var turboshake128 = /* @__PURE__ */ genTurboshake(168, 256 / 8);
  var turboshake256 = /* @__PURE__ */ genTurboshake(136, 512 / 8);
  function rightEncodeK12(n) {
    const res = [];
    for (; n > 0; n >>= 8)
      res.unshift(n & 255);
    res.push(res.length);
    return new Uint8Array(res);
  }
  var EMPTY = new Uint8Array([]);
  var KangarooTwelve = class _KangarooTwelve extends Keccak {
    constructor(blockLen, leafLen, outputLen, rounds, opts) {
      super(blockLen, 7, outputLen, true, rounds);
      this.leafLen = leafLen;
      this.chunkLen = 8192;
      this.chunkPos = 0;
      this.chunksDone = 0;
      const { personalization } = opts;
      this.personalization = toBytesOptional(personalization);
    }
    update(data) {
      data = toBytes(data);
      const { chunkLen, blockLen, leafLen, rounds } = this;
      for (let pos = 0, len = data.length; pos < len; ) {
        if (this.chunkPos == chunkLen) {
          if (this.leafHash)
            super.update(this.leafHash.digest());
          else {
            this.suffix = 6;
            super.update(new Uint8Array([3, 0, 0, 0, 0, 0, 0, 0]));
          }
          this.leafHash = new Keccak(blockLen, 11, leafLen, false, rounds);
          this.chunksDone++;
          this.chunkPos = 0;
        }
        const take = Math.min(chunkLen - this.chunkPos, len - pos);
        const chunk = data.subarray(pos, pos + take);
        if (this.leafHash)
          this.leafHash.update(chunk);
        else
          super.update(chunk);
        this.chunkPos += take;
        pos += take;
      }
      return this;
    }
    finish() {
      if (this.finished)
        return;
      const { personalization } = this;
      this.update(personalization).update(rightEncodeK12(personalization.length));
      if (this.leafHash) {
        super.update(this.leafHash.digest());
        super.update(rightEncodeK12(this.chunksDone));
        super.update(new Uint8Array([255, 255]));
      }
      super.finish.call(this);
    }
    destroy() {
      super.destroy.call(this);
      if (this.leafHash)
        this.leafHash.destroy();
      this.personalization = EMPTY;
    }
    _cloneInto(to) {
      const { blockLen, leafLen, leafHash, outputLen, rounds } = this;
      to || (to = new _KangarooTwelve(blockLen, leafLen, outputLen, rounds, {}));
      super._cloneInto(to);
      if (leafHash)
        to.leafHash = leafHash._cloneInto(to.leafHash);
      to.personalization.set(this.personalization);
      to.leafLen = this.leafLen;
      to.chunkPos = this.chunkPos;
      to.chunksDone = this.chunksDone;
      return to;
    }
    clone() {
      return this._cloneInto();
    }
  };
  var k12 = /* @__PURE__ */ (() => wrapConstructorWithOpts((opts = {}) => new KangarooTwelve(168, 32, chooseLen(opts, 32), 12, opts)))();
  var m14 = /* @__PURE__ */ (() => wrapConstructorWithOpts((opts = {}) => new KangarooTwelve(136, 64, chooseLen(opts, 64), 14, opts)))();

  // node_modules/@noble/hashes/esm/sha1.js
  var rotl3 = (word, shift) => word << shift | word >>> 32 - shift >>> 0;
  var Chi2 = (a, b, c) => a & b ^ ~a & c;
  var Maj2 = (a, b, c) => a & b ^ a & c ^ b & c;
  var IV4 = /* @__PURE__ */ new Uint32Array([
    1732584193,
    4023233417,
    2562383102,
    271733878,
    3285377520
  ]);
  var SHA1_W = /* @__PURE__ */ new Uint32Array(80);
  var SHA1 = class extends SHA2 {
    constructor() {
      super(64, 20, 8, false);
      this.A = IV4[0] | 0;
      this.B = IV4[1] | 0;
      this.C = IV4[2] | 0;
      this.D = IV4[3] | 0;
      this.E = IV4[4] | 0;
    }
    get() {
      const { A, B, C, D, E } = this;
      return [A, B, C, D, E];
    }
    set(A, B, C, D, E) {
      this.A = A | 0;
      this.B = B | 0;
      this.C = C | 0;
      this.D = D | 0;
      this.E = E | 0;
    }
    process(view, offset) {
      for (let i = 0; i < 16; i++, offset += 4)
        SHA1_W[i] = view.getUint32(offset, false);
      for (let i = 16; i < 80; i++)
        SHA1_W[i] = rotl3(SHA1_W[i - 3] ^ SHA1_W[i - 8] ^ SHA1_W[i - 14] ^ SHA1_W[i - 16], 1);
      let { A, B, C, D, E } = this;
      for (let i = 0; i < 80; i++) {
        let F, K;
        if (i < 20) {
          F = Chi2(B, C, D);
          K = 1518500249;
        } else if (i < 40) {
          F = B ^ C ^ D;
          K = 1859775393;
        } else if (i < 60) {
          F = Maj2(B, C, D);
          K = 2400959708;
        } else {
          F = B ^ C ^ D;
          K = 3395469782;
        }
        const T = rotl3(A, 5) + F + E + K + SHA1_W[i] | 0;
        E = D;
        D = C;
        C = rotl3(B, 30);
        B = A;
        A = T;
      }
      A = A + this.A | 0;
      B = B + this.B | 0;
      C = C + this.C | 0;
      D = D + this.D | 0;
      E = E + this.E | 0;
      this.set(A, B, C, D, E);
    }
    roundClean() {
      SHA1_W.fill(0);
    }
    destroy() {
      this.set(0, 0, 0, 0, 0);
      this.buffer.fill(0);
    }
  };
  var sha1 = /* @__PURE__ */ wrapConstructor(() => new SHA1());

  // node_modules/@noble/hashes/esm/argon2.js
  var ARGON2_SYNC_POINTS = 4;
  var toBytesOptional2 = (buf) => buf !== void 0 ? toBytes(buf) : new Uint8Array([]);
  function mul(a, b) {
    const aL = a & 65535;
    const aH = a >>> 16;
    const bL = b & 65535;
    const bH = b >>> 16;
    const ll = Math.imul(aL, bL);
    const hl = Math.imul(aH, bL);
    const lh = Math.imul(aL, bH);
    const hh = Math.imul(aH, bH);
    const BUF4 = (ll >>> 16) + (hl & 65535) + lh | 0;
    const h = (hl >>> 16) + (BUF4 >>> 16) + hh | 0;
    return { h, l: BUF4 << 16 | ll & 65535 };
  }
  function relPos(areaSize, relativePos) {
    return areaSize - 1 - mul(areaSize, mul(relativePos, relativePos).h).h;
  }
  function mul2(a, b) {
    const { h, l } = mul(a, b);
    return { h: (h << 1 | l >>> 31) & 4294967295, l: l << 1 & 4294967295 };
  }
  function blamka(Ah, Al, Bh, Bl) {
    const { h: Ch, l: Cl } = mul2(Al, Bl);
    const Rll = add3L(Al, Bl, Cl);
    return { h: add3H(Rll, Ah, Bh, Ch), l: Rll | 0 };
  }
  var BUF3 = new Uint32Array(256);
  function G(a, b, c, d) {
    let Al = BUF3[2 * a], Ah = BUF3[2 * a + 1];
    let Bl = BUF3[2 * b], Bh = BUF3[2 * b + 1];
    let Cl = BUF3[2 * c], Ch = BUF3[2 * c + 1];
    let Dl = BUF3[2 * d], Dh = BUF3[2 * d + 1];
    ({ h: Ah, l: Al } = blamka(Ah, Al, Bh, Bl));
    ({ Dh, Dl } = { Dh: Dh ^ Ah, Dl: Dl ^ Al });
    ({ Dh, Dl } = { Dh: rotr32H(Dh, Dl), Dl: rotr32L(Dh, Dl) });
    ({ h: Ch, l: Cl } = blamka(Ch, Cl, Dh, Dl));
    ({ Bh, Bl } = { Bh: Bh ^ Ch, Bl: Bl ^ Cl });
    ({ Bh, Bl } = { Bh: rotrSH(Bh, Bl, 24), Bl: rotrSL(Bh, Bl, 24) });
    ({ h: Ah, l: Al } = blamka(Ah, Al, Bh, Bl));
    ({ Dh, Dl } = { Dh: Dh ^ Ah, Dl: Dl ^ Al });
    ({ Dh, Dl } = { Dh: rotrSH(Dh, Dl, 16), Dl: rotrSL(Dh, Dl, 16) });
    ({ h: Ch, l: Cl } = blamka(Ch, Cl, Dh, Dl));
    ({ Bh, Bl } = { Bh: Bh ^ Ch, Bl: Bl ^ Cl });
    ({ Bh, Bl } = { Bh: rotrBH(Bh, Bl, 63), Bl: rotrBL(Bh, Bl, 63) });
    BUF3[2 * a] = Al, BUF3[2 * a + 1] = Ah;
    BUF3[2 * b] = Bl, BUF3[2 * b + 1] = Bh;
    BUF3[2 * c] = Cl, BUF3[2 * c + 1] = Ch;
    BUF3[2 * d] = Dl, BUF3[2 * d + 1] = Dh;
  }
  function P(v00, v01, v02, v03, v04, v05, v06, v07, v08, v09, v10, v11, v12, v13, v14, v15) {
    G(v00, v04, v08, v12);
    G(v01, v05, v09, v13);
    G(v02, v06, v10, v14);
    G(v03, v07, v11, v15);
    G(v00, v05, v10, v15);
    G(v01, v06, v11, v12);
    G(v02, v07, v08, v13);
    G(v03, v04, v09, v14);
  }
  function block(x, xPos, yPos, outPos, needXor) {
    for (let i = 0; i < 256; i++)
      BUF3[i] = x[xPos + i] ^ x[yPos + i];
    for (let i = 0; i < 128; i += 16) {
      P(i, i + 1, i + 2, i + 3, i + 4, i + 5, i + 6, i + 7, i + 8, i + 9, i + 10, i + 11, i + 12, i + 13, i + 14, i + 15);
    }
    for (let i = 0; i < 16; i += 2) {
      P(i, i + 1, i + 16, i + 17, i + 32, i + 33, i + 48, i + 49, i + 64, i + 65, i + 80, i + 81, i + 96, i + 97, i + 112, i + 113);
    }
    if (needXor)
      for (let i = 0; i < 256; i++)
        x[outPos + i] ^= BUF3[i] ^ x[xPos + i] ^ x[yPos + i];
    else
      for (let i = 0; i < 256; i++)
        x[outPos + i] = BUF3[i] ^ x[xPos + i] ^ x[yPos + i];
  }
  function Hp(A, dkLen) {
    const A8 = u8(A);
    const T = new Uint32Array(1);
    const T8 = u8(T);
    T[0] = dkLen;
    if (dkLen <= 64)
      return blake2b.create({ dkLen }).update(T8).update(A8).digest();
    const out = new Uint8Array(dkLen);
    let V = blake2b.create({}).update(T8).update(A8).digest();
    let pos = 0;
    out.set(V.subarray(0, 32));
    pos += 32;
    for (; dkLen - pos > 64; pos += 32)
      out.set((V = blake2b(V)).subarray(0, 32), pos);
    out.set(blake2b(V, { dkLen: dkLen - pos }), pos);
    return u32(out);
  }
  function indexAlpha(r, s, laneLen, segmentLen, index, randL, sameLane = false) {
    let area;
    if (0 == r) {
      if (0 == s)
        area = index - 1;
      else if (sameLane)
        area = s * segmentLen + index - 1;
      else
        area = s * segmentLen + (index == 0 ? -1 : 0);
    } else if (sameLane)
      area = laneLen - segmentLen + index - 1;
    else
      area = laneLen - segmentLen + (index == 0 ? -1 : 0);
    const startPos = r !== 0 && s !== ARGON2_SYNC_POINTS - 1 ? (s + 1) * segmentLen : 0;
    const rel = relPos(area, randL);
    return (startPos + rel) % laneLen;
  }
  function argon2Init(type, password, salt, opts) {
    password = toBytes(password);
    salt = toBytes(salt);
    let { p, dkLen, m, t, version, key, personalization, maxmem, onProgress } = {
      ...opts,
      version: opts.version || 19,
      dkLen: opts.dkLen || 32,
      maxmem: 2 ** 32
    };
    number(p);
    number(dkLen);
    number(m);
    number(t);
    number(version);
    if (dkLen < 4 || dkLen >= 2 ** 32)
      throw new Error("Argon2: dkLen should be at least 4 bytes");
    if (p < 1 || p >= 2 ** 32)
      throw new Error("Argon2: p (parallelism) should be at least 1");
    if (t < 1 || t >= 2 ** 32)
      throw new Error("Argon2: t (iterations) should be at least 1");
    if (m < 8 * p)
      throw new Error(`Argon2: memory should be at least 8*p bytes`);
    if (version !== 16 && version !== 19)
      throw new Error(`Argon2: unknown version=${version}`);
    password = toBytes(password);
    if (password.length < 0 || password.length >= 2 ** 32)
      throw new Error("Argon2: password should be less than 4 GB");
    salt = toBytes(salt);
    if (salt.length < 8)
      throw new Error("Argon2: salt should be at least 8 bytes");
    key = toBytesOptional2(key);
    personalization = toBytesOptional2(personalization);
    if (onProgress !== void 0 && typeof onProgress !== "function")
      throw new Error("progressCb should be function");
    const lanes = p;
    const mP = 4 * p * Math.floor(m / (ARGON2_SYNC_POINTS * p));
    const laneLen = Math.floor(mP / p);
    const segmentLen = Math.floor(laneLen / ARGON2_SYNC_POINTS);
    const h = blake2b.create({});
    const BUF4 = new Uint32Array(1);
    const BUF8 = u8(BUF4);
    for (const i of [p, dkLen, m, t, version, type]) {
      if (i < 0 || i >= 2 ** 32)
        throw new Error(`Argon2: wrong parameter=${i}, expected uint32`);
      BUF4[0] = i;
      h.update(BUF8);
    }
    for (let i of [password, salt, key, personalization]) {
      BUF4[0] = i.length;
      h.update(BUF8).update(i);
    }
    const H0 = new Uint32Array(18);
    const H0_8 = u8(H0);
    h.digestInto(H0_8);
    const memUsed = mP * 256;
    if (memUsed < 0 || memUsed >= 2 ** 32 || memUsed > maxmem) {
      throw new Error(`Argon2: wrong params (memUsed=${memUsed} maxmem=${maxmem}), should be less than 2**32`);
    }
    const B = new Uint32Array(memUsed);
    for (let l = 0; l < p; l++) {
      const i = 256 * laneLen * l;
      H0[17] = l;
      H0[16] = 0;
      B.set(Hp(H0, 1024), i);
      H0[16] = 1;
      B.set(Hp(H0, 1024), i + 256);
    }
    let perBlock = () => {
    };
    if (onProgress) {
      const totalBlock = t * ARGON2_SYNC_POINTS * p * segmentLen;
      const callbackPer = Math.max(Math.floor(totalBlock / 1e4), 1);
      let blockCnt = 0;
      perBlock = () => {
        blockCnt++;
        if (onProgress && (!(blockCnt % callbackPer) || blockCnt === totalBlock))
          onProgress(blockCnt / totalBlock);
      };
    }
    return { type, mP, p, t, version, B, laneLen, lanes, segmentLen, dkLen, perBlock };
  }
  function argon2Output(B, p, laneLen, dkLen) {
    const B_final = new Uint32Array(256);
    for (let l = 0; l < p; l++)
      for (let j = 0; j < 256; j++)
        B_final[j] ^= B[256 * (laneLen * l + laneLen - 1) + j];
    return u8(Hp(B_final, dkLen));
  }
  function processBlock(B, address, l, r, s, index, laneLen, segmentLen, lanes, offset, prev, dataIndependent, needXor) {
    if (offset % laneLen)
      prev = offset - 1;
    let randL, randH;
    if (dataIndependent) {
      if (index % 128 === 0) {
        address[256 + 12]++;
        block(address, 256, 2 * 256, 0, false);
        block(address, 0, 2 * 256, 0, false);
      }
      randL = address[2 * (index % 128)];
      randH = address[2 * (index % 128) + 1];
    } else {
      const T = 256 * prev;
      randL = B[T];
      randH = B[T + 1];
    }
    const refLane = r === 0 && s === 0 ? l : randH % lanes;
    const refPos = indexAlpha(r, s, laneLen, segmentLen, index, randL, refLane == l);
    const refBlock = laneLen * refLane + refPos;
    block(B, 256 * prev, 256 * refBlock, offset * 256, needXor);
  }
  function argon2(type, password, salt, opts) {
    const { mP, p, t, version, B, laneLen, lanes, segmentLen, dkLen, perBlock } = argon2Init(type, password, salt, opts);
    const address = new Uint32Array(3 * 256);
    address[256 + 6] = mP;
    address[256 + 8] = t;
    address[256 + 10] = type;
    for (let r = 0; r < t; r++) {
      const needXor = r !== 0 && version === 19;
      address[256 + 0] = r;
      for (let s = 0; s < ARGON2_SYNC_POINTS; s++) {
        address[256 + 4] = s;
        const dataIndependent = type == 1 || type == 2 && r === 0 && s < 2;
        for (let l = 0; l < p; l++) {
          address[256 + 2] = l;
          address[256 + 12] = 0;
          let startPos = 0;
          if (r === 0 && s === 0) {
            startPos = 2;
            if (dataIndependent) {
              address[256 + 12]++;
              block(address, 256, 2 * 256, 0, false);
              block(address, 0, 2 * 256, 0, false);
            }
          }
          let offset = l * laneLen + s * segmentLen + startPos;
          let prev = offset % laneLen ? offset - 1 : offset + laneLen - 1;
          for (let index = startPos; index < segmentLen; index++, offset++, prev++) {
            perBlock();
            processBlock(B, address, l, r, s, index, laneLen, segmentLen, lanes, offset, prev, dataIndependent, needXor);
          }
        }
      }
    }
    return argon2Output(B, p, laneLen, dkLen);
  }
  var argon2id = (password, salt, opts) => argon2(2, password, salt, opts);

  // node_modules/@noble/hashes/esm/eskdf.js
  var SCRYPT_FACTOR = 2 ** 19;
  var PBKDF2_FACTOR = 2 ** 17;
  function scrypt2(password, salt) {
    return scrypt(password, salt, { N: SCRYPT_FACTOR, r: 8, p: 1, dkLen: 32 });
  }
  function pbkdf22(password, salt) {
    return pbkdf2(sha256, password, salt, { c: PBKDF2_FACTOR, dkLen: 32 });
  }
  function xor32(a, b) {
    bytes(a, 32);
    bytes(b, 32);
    const arr = new Uint8Array(32);
    for (let i = 0; i < 32; i++) {
      arr[i] = a[i] ^ b[i];
    }
    return arr;
  }
  function strHasLength(str, min, max) {
    return typeof str === "string" && str.length >= min && str.length <= max;
  }
  function deriveMainSeed(username, password) {
    if (!strHasLength(username, 8, 255))
      throw new Error("invalid username");
    if (!strHasLength(password, 8, 255))
      throw new Error("invalid password");
    const scr = scrypt2(password + "", username + "");
    const pbk = pbkdf22(password + "", username + "");
    const res = xor32(scr, pbk);
    scr.fill(0);
    pbk.fill(0);
    return res;
  }
  function getSaltInfo(protocol, accountId = 0) {
    if (!(strHasLength(protocol, 3, 15) && /^[a-z0-9]{3,15}$/.test(protocol))) {
      throw new Error("invalid protocol");
    }
    const allowsStr = /^password\d{0,3}|ssh|tor|file$/.test(protocol);
    let salt;
    if (typeof accountId === "string") {
      if (!allowsStr)
        throw new Error("accountId must be a number");
      if (!strHasLength(accountId, 1, 255))
        throw new Error("accountId must be valid string");
      salt = toBytes(accountId);
    } else if (Number.isSafeInteger(accountId)) {
      if (accountId < 0 || accountId > 2 ** 32 - 1)
        throw new Error("invalid accountId");
      salt = new Uint8Array(4);
      createView(salt).setUint32(0, accountId, false);
    } else {
      throw new Error(`accountId must be a number${allowsStr ? " or string" : ""}`);
    }
    const info = toBytes(protocol);
    return { salt, info };
  }
  function countBytes(num) {
    if (typeof num !== "bigint" || num <= BigInt(128))
      throw new Error("invalid number");
    return Math.ceil(num.toString(2).length / 8);
  }
  function getKeyLength(options) {
    if (!options || typeof options !== "object")
      return 32;
    const hasLen = "keyLength" in options;
    const hasMod = "modulus" in options;
    if (hasLen && hasMod)
      throw new Error("cannot combine keyLength and modulus options");
    if (!hasLen && !hasMod)
      throw new Error("must have either keyLength or modulus option");
    const l = hasMod ? countBytes(options.modulus) + 8 : options.keyLength;
    if (!(typeof l === "number" && l >= 16 && l <= 8192))
      throw new Error("invalid keyLength");
    return l;
  }
  function modReduceKey(key, modulus) {
    const _1 = BigInt(1);
    const num = BigInt("0x" + bytesToHex(key));
    const res = num % (modulus - _1) + _1;
    if (res < _1)
      throw new Error("expected positive number");
    const len = key.length - 8;
    const hex = res.toString(16).padStart(len * 2, "0");
    const bytes2 = hexToBytes(hex);
    if (bytes2.length !== len)
      throw new Error("invalid length of result key");
    return bytes2;
  }
  async function eskdf(username, password) {
    let seed = deriveMainSeed(username, password);
    function deriveCK(protocol, accountId = 0, options) {
      bytes(seed, 32);
      const { salt, info } = getSaltInfo(protocol, accountId);
      const keyLength = getKeyLength(options);
      const key = hkdf(sha256, seed, salt, info, keyLength);
      return options && "modulus" in options ? modReduceKey(key, options.modulus) : key;
    }
    function expire() {
      if (seed)
        seed.fill(1);
      seed = void 0;
    }
    const fingerprint = Array.from(deriveCK("fingerprint", 0)).slice(0, 6).map((char) => char.toString(16).padStart(2, "0").toUpperCase()).join(":");
    return Object.freeze({ deriveChildKey: deriveCK, expire, fingerprint });
  }

  // input.js
  var utils = { bytesToHex, randomBytes };
  return __toCommonJS(input_exports);
});

function sha512() {
    return nobleHashes().sha512;
}

export { sha512 };

/*! Bundled license information:

@noble/hashes/esm/utils.js:
  (*! noble-hashes - MIT License (c) 2022 Paul Miller (paulmillr.com) *)
*/
