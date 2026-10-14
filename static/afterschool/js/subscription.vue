<!-- This file is part of Happyschool. -->
<!--  -->
<!-- Happyschool is the legal property of its developers, whose names -->
<!-- can be found in the AUTHORS file distributed with this source -->
<!-- distribution. -->
<!--  -->
<!-- Happyschool is free software: you can redistribute it and/or modify -->
<!-- it under the terms of the GNU Affero General Public License as published by -->
<!-- the Free Software Foundation, either version 3 of the License, or -->
<!-- (at your option) any later version. -->
<!--  -->
<!-- Happyschool is distributed in the hope that it will be useful, -->
<!-- but WITHOUT ANY WARRANTY; without even the implied warranty of -->
<!-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the -->
<!-- GNU Affero General Public License for more details. -->
<!--  -->
<!-- You should have received a copy of the GNU Affero General Public License -->
<!-- along with Happyschool.  If not, see <http://www.gnu.org/licenses/>. -->

<template>
    <BCard title="Inscription">
        <BCardBody v-if="activity">
            <BButton
                to="/"
                variant="outline-secondary"
            >
                <b-icon icon="arrow-left" />
                Retour
            </BButton>
            <h3>{{ activity.name }}</h3>
            <p class="bg-light">
                Le <strong>{{ days[activity.day] }}
                    <span v-if="activity.next_week_sub">{{ nextSubDay.toLocaleString() }}</span>
                </strong>.
            </p>
            <p>{{ activity.description }}</p>
            <h4>Formulaire d'inscription</h4>
            <BForm @submit.stop.prevent="onSubmit">
                <BFormGroup
                    label="Nom de l'élève"
                >
                    <BInput
                        v-model="v$.form.student_lastname.$model"
                        :state="validateState('student_lastname')"
                    />
                    <BFormInvalidFeedback>
                        Le nom de l'élève est nécessaire.
                    </BFormInvalidFeedback>
                </BFormGroup>
                <BFormGroup
                    label="Prénom de l'élève"
                >
                    <BInput
                        v-model="v$.form.student_firstname.$model"
                        :state="validateState('student_firstname')"
                    />
                    <BFormInvalidFeedback>
                        Le prénom de l'élève est nécessaire.
                    </BFormInvalidFeedback>
                </BFormGroup>
                <BFormGroup
                    label="Classe de l'élève (dernière classe)"
                >
                    <BInput
                        v-model="v$.form.classe.$model"
                        :state="validateState('classe')"
                    />
                    <BFormInvalidFeedback>
                        La classe de l'élève est nécessaire.
                    </BFormInvalidFeedback>
                </BFormGroup>
                <BFormGroup
                    label="Date de naissance de l'élève"
                >
                    <BInput
                        type="date"
                        v-model="v$.form.birth.$model"
                        :state="validateState('birth')"
                    />
                    <BFormInvalidFeedback>
                        La date de naissance de l'élève est nécessaire.
                    </BFormInvalidFeedback>
                </BFormGroup>
                <BFormGroup
                    label=" Autre(s) frère(s) ou sœur(s) inscrit(s) à un atelier (noms et prénoms)"
                >
                    <BInput
                        v-model="v$.form.family.$model"
                        :state="validateState('family')"
                    />
                </BFormGroup>
                <BFormGroup
                    label="Nom du responsable"
                >
                    <BInput
                        v-model="v$.form.resp_lastname.$model"
                        :state="validateState('resp_lastname')"
                    />
                    <BFormInvalidFeedback>
                        Le nom du responsable est nécessaire.
                    </BFormInvalidFeedback>
                </BFormGroup>
                <BFormGroup
                    label="Prénom du responsable"
                >
                    <BInput
                        v-model="v$.form.resp_firstname.$model"
                        :state="validateState('resp_firstname')"
                    />
                    <BFormInvalidFeedback>
                        Le prénom du responsable est nécessaire.
                    </BFormInvalidFeedback>
                </BFormGroup>
                <BFormGroup
                    label="Téléphone du responsable"
                >
                    <BInput
                        v-model="v$.form.resp_phone.$model"
                        :state="validateState('resp_phone')"
                    />
                    <BFormInvalidFeedback>
                        Le téléphone du responsable est nécessaire.
                    </BFormInvalidFeedback>
                </BFormGroup>
                <BFormGroup
                    label="Téléphone secondaire"
                >
                    <BInput
                        v-model="v$.form.resp_phone_2.$model"
                        :state="validateState('resp_phone_2')"
                    />
                </BFormGroup>
                <BFormGroup
                    label="Courriel du responsable"
                >
                    <BInput
                        v-model="v$.form.resp_email.$model"
                        :state="validateState('resp_email')"
                    />
                    <BFormInvalidFeedback>
                        Le courriel du responsable est nécessaire.
                    </BFormInvalidFeedback>
                </BFormGroup>
                <BFormGroup
                    label="Choix pour le paiement"
                    v-if="false"
                >
                    <BFormRadioGroup
                        stacked
                        v-model="v$.form.resp_payement.$model"
                        :options="payements"
                        :state="validateState('resp_payement')"
                    >
                        <BFormInvalidFeedback :state="validateState('resp_payement')">
                            Vous devez choisir un mode de paiement.
                        </BFormInvalidFeedback>
                    </BFormRadioGroup>
                </BFormGroup>
                <BFormGroup>
                    <BFormCheckbox
                        v-model="agree"
                    >
                        J'inscris mon enfant à cette activité et confirme avoir pris connaissance des dispositions pratiques.
                    </BFormCheckbox>
                </BFormGroup>
                <b-overlay :show="sending">
                    <b-button
                        type="submit"
                        variant="primary"
                        :disabled="!agree"
                    >
                        Envoyer l'inscription
                    </b-button>
                </b-overlay>
            </BForm>
        </BCardBody>
    </BCard>
</template>

<script>
import axios from "axios";
import useVuelidate from "@vuelidate/core";
import { DateTime } from "luxon";
import { required, email } from "@vuelidate/validators";

import { useToast } from "bootstrap-vue-next";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    setup: function () {
        const { show } = useToast();

        return { v$: useVuelidate(), show };
    },
    props: {
        activityId: {
            type: Number,
            default: 1,
        },
    },
    data: function () {
        return {
            activity: null,
            sending: false,
            payements: [
                { text: "Paiement en une fois", value: "1x" },
                { text: "Paiement en deux fois (50% à l'inscription et 50% au plus tard le 15 janvier)", value: "2x" },
            ],
            days: {
                0: "Lundi",
                1: "Mardi",
                2: "Mercredi",
                3: "Jeudi",
                4: "Vendredi",
            },
            form: {
                activity: this.activityId,
                student_lastname: "",
                student_firstname: "",
                classe: "",
                birth: "",
                family: "",
                resp_lastname: "",
                resp_firstname: "",
                resp_phone: "",
                resp_phone_2: "",
                resp_email: "",
                resp_payement: "1x",
            },
            agree: false,
        };
    },
    computed: {
        nextSubDay: function () {
            const currentDT = DateTime.now();
            if (currentDT.weekday - 1 !== this.activity.day) {
                const deltaDays = (8 - (currentDT.weekday - this.activity.day)) % 7;
                return currentDT.plus({ days: deltaDays });
            }

            if (currentDT.hour >= 12) {
                return currentDT.plus({ days: 7 });
            }

            return currentDT;
        },
    },
    methods: {
        validateState: function (name) {
            const { $dirty, $error } = this.v$.form[name];
            if (!$dirty) return null;

            return !$error;
        },
        onSubmit: function () {
            this.v$.form.$touch();
            if (this.v$.form.$anyError) {
                return;
            }

            this.sending = true;
            axios.post("/afterschool/api/subscription/", this.form, token)
                .then(() => {
                    this.sending = false;
                    this.$router.push("/", () => {
                        this.show({
                            body: "La demande d'inscription a été validée. Un courriel de confirmation vous a été envoyée.",
                            variant: "success",
                            noCloseButton: true,
                        });
                    });
                })
                .catch((err) => {
                    console.log(err);
                    this.show({
                        body: "Une erreur est survenue lors de la demande d'inscription. Merci de vérifier que les données soumises sont correctes.",
                        variant: "danger",
                        noCloseButton: true,
                    });
                    this.sending = false;
                });
        },
    },
    validations() {
        return {
            form: {
                student_lastname: { required },
                student_firstname: { required },
                classe: { required },
                birth: { required },
                family: {},
                resp_lastname: { required },
                resp_firstname: { required },
                resp_phone: { required },
                resp_phone_2: { required },
                resp_email: { required, email },
                resp_payement: { required },
            },
        };
    },
    mounted: function () {
        axios.get(`/afterschool/api/activity/${this.activityId}/`)
            .then((resp) => {
                this.activity = resp.data;
            });
    },
};
</script>

<style>

</style>
