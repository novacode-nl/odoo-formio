// Copyright Nova Code (https://www.novacode.nl)
// See LICENSE file for full licensing details.

export function uuidv4() {
    // Used in cache invalidation (can also be used in PWA).
    // XXX: not ideal https://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(
        /[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

export function protectComponent(componentClass) {
    Object.freeze(componentClass.prototype);
}
