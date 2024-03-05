/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useBus, useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { useModel } from "@web/model/model";
import { RelationalModel } from "@web/model/relational_model/relational_model";
import { extractFieldsFromArchInfo } from "@web/model/relational_model/utils";
import { standardViewProps } from "@web/views/standard_view_props";
import { ViewButton } from "@web/views/view_button/view_button";
import { FormArchParser } from "@web/views/form/form_arch_parser";
import { FormCompiler } from "@web/views/form/form_compiler";
import { Component, useEffect, useState } from "@odoo/owl";

export class FormController extends Component {
    setup() {
        this.router = useService("router");
        this.orm = useService("orm");
        this.state = useState({
            isDisabled: false,
        });
        this.ui = useService("ui");
        useBus(this.ui.bus, "resize", this.render);

        this.archInfo = this.props.archInfo;
        const activeFields = this.archInfo.activeFields;
        const fields = this.props.fields;
        const mode = 'edit';

        const beforeFirstLoad = async () => {
            const { activeFields, fields } = extractFieldsFromArchInfo(
                this.archInfo,
                this.props.fields
            );
            this.model.config.activeFields = activeFields;
            this.model.config.fields = fields;
        };
        
        this.model = useState(useModel(this.props.Model, this.modelParams, { beforeFirstLoad }));
        this.display = { ...this.props.display };

        useEffect(() => {
            this.updateURL();
        });

        // scroll top (especially for wizard forms with long pages)
        window.addEventListener('message', function(event) {
            const baseUrl = window.location.protocol + '//' + window.location.host;
            if (event.data.hasOwnProperty('odooFormioMessage')) {
                const msg = event.data.odooFormioMessage,
                      params = event.data.params;
                if (event.origin == baseUrl && msg == 'formioScrollTop') {
                    document.getElementsByClassName('o_content', window.parent.document)[0].scrollTo(0, 0);
                }
            }
        }, false);
    }
    
    updateURL() {
        this.router.pushState({ id: this.model.root.resId || undefined });
    }

    get modelParams() {
        let mode = this.props.mode || "edit";
        if (!this.canEdit && this.props.resId) {
            mode = "readonly";
        }
        return {
            config: {
                resModel: this.props.resModel,
                resId: this.props.resId || false,
                fields: this.props.fields,
                activeFields: {}, // will be generated after loading sub views (see willStart)
                isMonoRecord: true,
                mode,
                context: this.props.context,
            },
            state: this.props.state?.modelState,
        };
    }
}

FormController.template = "formio.FormView";
FormController.components = {
    Layout,
    ViewButton,
};
FormController.props = {
    ...standardViewProps,
    Model: Function,
    Renderer: Function,
    Compiler: Function,
    archInfo: Object,
};

export class FormRenderer extends Component {
    setup() {
        super.setup();
    }
}

export const FormView = {
    type: "formio_form",
    display_name: "Form",
    icon: "fa fa-rocket",
    // multiRecord: true, // when false it shows viewButtons
    // multiRecord: false, // ideally to show viewButtons
    searchMenuTypes: [],
    Controller: FormController,
    Renderer: FormRenderer,
    Model: RelationalModel,
    ArchParser: FormArchParser,
    Compiler: FormCompiler,
    
    props: (genericProps, view) => {
        const { ArchParser } = view;
        const { arch, relatedModels, resModel } = genericProps;
        const archInfo = new ArchParser().parse(arch, relatedModels, resModel);
        let modelParams = genericProps.state;
        if (!modelParams) {
            const { arch,  resModel, fields, context} = genericProps;
            modelParams = {
                context: context,
                fields: fields,
            };
        }
        return {
            ...genericProps,
            Model: view.Model,
            Renderer: view.Renderer,
            Compiler: view.Compiler,
            archInfo,
        };
    },
};

registry.category("views").add('formio_form', FormView);
