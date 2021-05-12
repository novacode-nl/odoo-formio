odoo.define('formio.tour', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');

    var _t = core._t;

    tour.register("formio_tour", {
        url: "/web",
        rainbowMan: false,
        sequence: 20,
    }, [{
        trigger: "button[name='action_view_formio']",
        content: _t("After save, click here (or the view switch) to open the Form Builder."),
        position: "bottom",
    }]);
});
