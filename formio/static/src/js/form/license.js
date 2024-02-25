// Copyright Nova Code (https://www.novacode.nl)
// See LICENSE file for full licensing details.

const { protectComponent, uuidv4 } = await import('./utils.js');

// random import path ensures no caching
const pathNobleEd25519 = "/formio/static/lib/noble-ed25519.min.js?" + uuidv4();
const pathNobleHashes = "/formio/static/lib/noble-hashes.js?" + uuidv4();

const ed = await import(pathNobleEd25519);
const { sha512 } = await import(pathNobleHashes);

const base64ToArray = (b64) => {
    return Uint8Array.from(atob(b64), c => c.charCodeAt(0));
};

ed.etc.sha512Sync = (...m) => sha512().create().update(ed.etc.concatBytes(...m)).digest();

const { Component } = owl;

export class License extends Component {

    isValidLicense(licenses) {
        const self = this;
        const valid = true;
	const b64Pubkey = 'XzgyMhhjCqmWiiB0Z3fR15dNpmtTeRK1aLaQww9mXRo=';
        for (let i = 0; i < licenses.length; i++) {
            const licenseKey = licenses[i];
            try {
	        const [json, b64Signature] = licenseKey.split('#');
                const licenseProps = JSON.parse(json);
	        const binPubkey = base64ToArray(b64Pubkey);
	        const hexPubkey = ed.etc.bytesToHex(binPubkey);
	        const binSignature = base64ToArray(b64Signature);
	        const hexSignature = ed.etc.bytesToHex(binSignature);
	        const binMessage = new TextEncoder().encode(json);
	        const hexMessage = ed.etc.bytesToHex(binMessage);
                const domains = licenseProps.domains;
                const validUntil = licenseProps.validUntil;

                if (ed.verify(binSignature, binMessage, binPubkey)) {
                    if (domains.includes(document.location.hostname)
                        && self.isValidUntil(new Date(validUntil), new Date())) {
                        return true;
                    }
                    else if (!domains.includes(document.location.hostname)) {
                        console.log('License: invalid domain ' + document.location.hostname);
                    }
                    else if (self.isValidUntil(new Date(validUntil), new Date())) {
                        console.log('License: invalid validUntil date ' + validUntil);
                    }
                }
                else {
                    console.log('License: invalid signature: ' + b64Signature);
                }
            } catch (error) {
                console.log('License error: ' + error);
            }
        }
        return false;
    }

    isValidUntil(validUntil, today) {
        const dateValidUntil = new Date(validUntil);
        dateValidUntil.setHours(0, 0, 0, 0);
        const dateToday = new Date(today);
        dateToday.setHours(0, 0, 0, 0);
        return dateValidUntil.getTime() >= dateToday.getTime();
    }
}

protectComponent(License);
