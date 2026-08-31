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
    <BRow>
        <BCol>
            <h2>Activités</h2>
        </BCol>
    </BRow>
    <BRow v-if="store.settings.show_by_teaching">
        <BNav pills>
            <BNavItem
                v-for="t in teachings"
                :key="t.id"
                :active="currentTeachingId === t.id"
                :to="`/activities/${t.id}/`"
            >
                {{ t.display_name }}
            </BNavItem>
        </BNav>
    </BRow>
    <BRow :cols-md="maxDays + 1">
        <BCol
            v-for="(day, index) in activitiesByDay"
            :key="index"
            cols="12"
        >
            <h3 class="text-center">
                {{ days[index] }}
            </h3>
            <BCard
                v-for="a in day"
                :key="a.id"
                no-body
                class="mb-3 activity"
            >
                <div class="date text-muted bg-light font-weight-bold">
                    {{ a.date_start }}
                    <b-icon icon="arrow-right" />
                    {{ a.date_stop }}
                </div>
                <div :class="`name text-white ${a.no_subscription ? 'bg-secondary' : 'bg-info'}`">
                    {{ a.name }}
                </div>
                <div class="age">
                    {{ a.age }}
                </div>
                <div class="timerange">
                    <em>{{ a.timerange }}</em>
                </div>
                <div class="animator">
                    <em>{{ a.animator }}</em>
                </div>
                <div v-if="!a.no_subscription">
                    <BButton
                        block
                        squared
                        variant="outline-primary"
                        :to="`/subscription/${a.id}/`"
                    >
                        <b-icon icon="box-arrow-in-right" /> S'inscrire
                    </BButton>
                </div>
            </BCard>
        </BCol>
    </BRow>
</template>

<script>
import axios from "axios";

import { afterSchoolStore } from "./store.js";

export default {
    props: {
        currentTeachingId: {
            type: Number,
            default: () => {
                // eslint-disable-next-line no-undef
                return settings.teachings[0];
            },
        },
    },
    data: function () {
        return {
            canViewSubscriptions: false,
            teachings: [],
            activities: [],
            // activitiesByDay: [],
            currentTeaching: null,
            days: {
                0: "Lundi",
                1: "Mardi",
                2: "Mercredi",
                3: "Jeudi",
                4: "Vendredi",
            },
            store: afterSchoolStore(),
        };
    },
    computed: {
        activityList: function () {
            if (this.store.settings.show_by_teaching) {
                return this.activities
                    .filter(a => a.teaching === this.currentTeachingId);
            }
            return this.activities;
        },
        maxDays: function () {
            return this.activityList
                .reduce((pV, cV) => Math.max(pV, cV.day), 1);
        },
        activitiesByDay: function () {
            let actByDay = Array(this.maxDays);
            this.activityList
                .forEach((a) => {
                    if (!Array.isArray(actByDay[a.day])) {
                        actByDay[a.day] = new Array();
                    }
                    actByDay[a.day].push(a);
                });
            return actByDay.map(d => d.sort((a, b) => a.priority <= b.priority));
        },
    },
    mounted: function () {
        if (this.store.settings.show_by_teaching) {
            Promise.all([axios.get("/core/api/teaching"), axios.get("/afterschool/api/activity")])
                .then((resp) => {
                    this.teachings = resp[0].data.results;
                    this.currentTeaching = this.teachings.find(t => t.id === this.currentTeachingId);
                    this.activities = resp[1].data.results;
                });
        } else {
            axios.get("/afterschool/api/activity")
                .then((resp) => {
                    this.activities = resp.data.results;
                });
        }
    },
};
</script>

<style>
.activity {
    text-align: center;
}

.name {
    font-size: 1.3em;
}
</style>
