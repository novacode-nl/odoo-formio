// Copyright Nova Code (https://www.novacode.nl)
// See LICENSE file for full licensing details.

const { protectComponent, uuidv4 } = await import('./utils.js');

const pathLicense = "./license.js?" + uuidv4();
let { License } = await import(pathLicense);

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
        const madeWithTranslations = {
            'en_US': 'Form made with',
            'ar': 'النموذج المصنوع من',
            'es': 'Formulario credo con',
            'hi_IN': 'द्वारा संभव बनाया गया',
            'it_IT': 'Modulo creato con',
            'ro_RO': 'Formular creat cu',
            'ru_RU': 'форма, созданная с помощью',
            'th_TH': 'แบบฟอร์มที่สร้างขึ้นด้วย',
            'zh_TW': '該表格是使用建立的',
            'zh': '表单是用创建的'
        };
        const tooltipTranslations = {
            'en_US': 'You can remove the Nova Forms branding by purchasing a license',
            'ar': 'يمكنك إزالة العلامة التجارية Nova Forms عن طريق شراء ترخيص',
            'de': 'Sie können das Nova Forms branding entfernen, indem Sie eine lizenz erwerben',
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
        let madeWith = madeWithTranslations['en_US'];
        if (madeWithTranslations.hasOwnProperty(language)) {
            madeWith = madeWithTranslations[language];
        }
        else if (madeWithTranslations.hasOwnProperty(languageShort)) {
            madeWith = madeWithTranslations[languageShort];
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
            <a href="https://www.novaforms.app" target="_blank" data-tooltip="${tooltip}"
                style="display: inline-block !important; margin-bottom: 1px !important; padding: 4px 8px 4px 8px !important; border: 2px solid #c0c0c0 !important; border-radius: 5px !important; background-color: #fff !important; color: #000 !important; font-size: 1.1rem !important; text-decoration-thickness: 0.1rem !important;">
                ${madeWith} <span style="color: #aa4689 !important; font-weight: bold !important; text-decoration-thickness: 0.1rem !important;" >Nova Forms</span>
            </a>
        `);
    }
}

protectComponent(Branding);
