import Vue from 'vue'
import Vuex from 'vuex'

import profile from './modules/profile'
import users from './modules/users'
import ingredients from "./modules/ingredients"
import pantry from "./modules/pantry"
import recipes from './modules/recipes'

Vue.use(Vuex)

export default new Vuex.Store({
	modules: {
		profile: {
			namespaced: true,
			state: profile.state,
			actions: profile.actions,
			getters: profile.getters,
			mutations: profile.mutations
		},
		users: {
			namespaced: true,
			state: users.state,
			actions: users.actions,
			getters: users.getters,
			mutations: users.mutations
		},
		ingredients: {
			namespaced: true,
			state: ingredients.state,
			actions: ingredients.actions,
			getters: ingredients.getters,
			mutations: ingredients.mutations
		},
		pantry: {
			namespaced: true,
			state: pantry.state,
			actions: pantry.actions,
			getters: pantry.getters,
			mutations: pantry.mutations
		},
		recipes: {
			namespaced: true,
			state: recipes.state,
			actions: recipes.actions,
			getters: recipes.getters,
			mutations: recipes.mutations
		}
	}
})
