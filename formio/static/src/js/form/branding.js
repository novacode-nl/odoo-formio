// Copyright Nova Code (https://www.novacode.nl)
// See LICENSE file for full licensing details.

function uuidv4() {
    // Used in cache invalidation (can also be used in PWA).
    // TODO: DRY, move to generic function/method to be imported here.
    // XXX: not ideal https://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(
        /[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

const importPathLicense = "./license.js?" + uuidv4();
let { License } = await import(importPathLicense);

const { Component, markup, onMounted, useState, xml } = owl;

export class Branding extends License {
    static template = xml`<div style="text-align: center !important; display: block !important;">
        <t t-out="state.output"/>
    </div>`;

    setup() {
        super.setup();
        this.state = useState({output: null});
        onMounted(() => {
            this.loadBranding();
        });
    }

    loadBranding() {
        const self = this;
        const licenseUrl = '/formio/license';

        this.props.getData(licenseUrl, {}).then(function(res) {
            if (!$.isEmptyObject(res) && !$.isEmptyObject(res['licenses'])) {
                if (!self.isValidLicense(res['licenses'])) {
                    self.renderBranding(res['language']);
                }
            }
            else {
                self.renderBranding(res['language']);
            }
        });
    }

    renderBranding(language) {
        const languageShort = language.substring(0, 2);

        // translations (en_US is default)
        const poweredByTranslations = {
            'en_US': 'Form powered by',
            'ar': 'النموذج مدعوم من',
            'es': 'Formulario impulsado por',
            'hi_IN': 'द्वारा संभव बनाया गया',
            'it_IT': 'Modulo alimentato da',
            'ro_RO': 'Formular alimentat de',
            'ru_RU': 'Форма стала возможной благодаря',
            'th_TH': 'แบบฟอร์มขับเคลื่อนโดย',
            'zh_TW': '表格由',
            'zh': '表格由',
        };
        const tooltipTranslations = {
            'en_US': 'You can remove the Nova Forms branding by purchasing a license',
            'ar': 'يمكنك إزالة العلامة التجارية Nova Forms عن طريق شراء ترخيص',
            'de': 'Sie können das Nova Forms-Branding entfernen, indem Sie eine Lizenz erwerben',
            'es': 'Puede eliminar la marca Nova Forms comprando una licencia',
            'hi_IN': 'आप लाइसेंस खरीदकर नोवा फॉर्म ब्रांडिंग को हटा सकते हैं',
            'it_IT': 'Puoi rimuovere il marchio Nova Forms acquistando una licenza',
            'ro_RO': 'Puteți elimina marca Nova Forms achiziționând o licență',
            'ru_RU': 'Вы можете удалить брендинг Nova Forms, купив лицензию.',
            'th_TH': 'คุณสามารถลบตราสินค้า Nova Forms ได้โดยการซื้อใบอนุญาต',
            'zh_TW': '您可以透過購買授權來刪除 Nova Forms 品牌',
            'zh': '您可以通过购买许可证来删除 Nova Forms 品牌'
        };

        // powered by
        let poweredBy = poweredByTranslations['en_US'];
        if (poweredByTranslations.hasOwnProperty(language)) {
            poweredBy = poweredByTranslations[language];
        }
        else if (poweredByTranslations.hasOwnProperty(languageShort)) {
            poweredBy = poweredByTranslations[languageShort];
        }

        // tooltip
        let tooltip = tooltipTranslations['en_US'];
        if (tooltipTranslations.hasOwnProperty(language)) {
            tooltip = tooltipTranslations[language];
        }
        else if (tooltipTranslations.hasOwnProperty(languageShort)) {
            tooltip = tooltipTranslations[languageShort];
        }

        this.state.output = markup(`
            <div data-tooltip="${tooltip}"
                style="display: inline-block !important; margin-bottom: 1px !important; padding: 4px 8px 4px 8px !important; border: 1px solid #c0c0c0 !important; border-radius: 5px !important; background-color: #fff !important; color: #000 !important;">
                ${poweredBy} <a style="color: #000 !important; font-weight: bold !important;" href="https://www.novaforms.app">Nova Forms</a>
            </div>
        `);
    }
}
