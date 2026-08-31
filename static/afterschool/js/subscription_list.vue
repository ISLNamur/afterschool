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
    <div>
        <BRow>
            <BCol>
                <h2>Liste des inscriptions</h2>
            </BCol>
        </BRow>
        <BRow class="mb-2">
            <BCol>
                <BButton href="/afterschool/file_list/">
                    Télécharger la liste (Excel)
                </BButton>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BCard
                    v-for="subscription in subscriptions"
                    :key="subscription.id"
                >
                    <ul>
                        <li>Élève (nom/prénom): {{ subscription.student_lastname }}/{{ subscription.student_firstname }}</li>
                        <li>Classe: {{ subscription.classe }}</li>
                        <li>Date de naissance: {{ subscription.birth }}</li>
                        <li>Autre personne de la famille: {{ subscription.family }}</li>
                        <li>Responsable (nom/prénom) : {{ subscription.resp_lastname }}/{{ subscription.resp_firstname }}</li>
                        <li>Responsable adresse : {{ subscription.resp_address }}</li>
                        <li>Responsable courriel : <a :href="`mailto:${subscription.resp_email}`">{{ subscription.resp_email }}</a></li>
                        <li>Responsable courriel 2 : <a :href="`mailto:${subscription.resp_email_2}`">{{ subscription.resp_email_2 }}</a></li>
                        <li>Responsable tél. : {{ subscription.resp_phone }}</li>
                        <li>Responsable tél. 2 : {{ subscription.resp_phone_2 }}</li>
                        <li>Paiement : {{ subscription.resp_payement }}</li>
                        <li>Activité : {{ getActivity(subscription.activity) }}</li>
                    </ul>
                </BCard>
            </BCol>
        </BRow>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data: function () {
        return {
            subscriptions: [],
            activities: [],
            days: {
                0: "Lundi",
                1: "Mardi",
                2: "Mercredi",
                3: "Jeudi",
                4: "Vendredi",
            },
        };
    },
    methods: {
        getActivity: function (activity) {
            const activityObject = this.activities.find(a => a.id === activity);
            if (!activityObject) return "";

            return `${activityObject.name} (
                ${this.days[activityObject.day]} entre ${activityObject.timerange}
                / ${activityObject.date_start} ${activityObject.date_stop}
            )`;
        },
    },
    mounted: function () {
        axios.get("/afterschool/api/activity/")
            .then((resp) => {
                this.activities = resp.data.results;
                axios.get("/afterschool/api/subscription/")
                    .then((resp) => {
                        this.subscriptions = resp.data.results;
                    });
            });
    },
};
</script>
