// This file is part of Happyschool.
//
// Happyschool is the legal property of its developers, whose names
// can be found in the AUTHORS file distributed with this source
// distribution.
//
// Happyschool is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Happyschool is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with Happyschool.  If not, see <http://www.gnu.org/licenses/>.

import AfterschoolPage from "./AfterSchoolPage.vue";
import Activities from "./activities.vue";
import Subscription from "./subscription.vue";
import SubscriptionList from "./subscription_list.vue";

import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
    routes: [
        {
            path: "/",
            component: Activities,
        },
        {
            path: "/activities/:currentTeachingId/",
            component: Activities,
            props: (route) => {
                const props = { ...route.params };
                props.currentTeachingId = Number(props.currentTeachingId);
                return props;
            },
        },
        {
            path: "/subscription/:activityId/",
            component: Subscription,
            props: (route) => {
                const props = { ...route.params };
                props.activityId = Number(props.activityId);
                return props;
            },
        },
        {
            path: "/subscription_list/",
            component: SubscriptionList,
        },
    ],
    history: createWebHashHistory(),
});

export default router;
