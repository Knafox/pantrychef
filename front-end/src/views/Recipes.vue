<template>
	<div>
		<div class="row">
			<div class="col-lg-12">
				<h1 class="mt-4">Recipes</h1>
			</div>
		</div>
		<div class="row">
			<div v-for="i in recipes" v-bind:key="i.name">
				<recipe-card :recipe="i" v-if="i.id"></recipe-card>
			</div>
		</div>
	</div>
</template>

<script>
import RecipeCard from '../components/RecipeCard'
import ViewRecipe from './ViewRecipe'

import { mapGetters, mapActions } from 'vuex'

export default {
	name: 'recipes',
	computed: {
		...mapGetters('recipes', {
			recipes: 'recipes'
		}),
		...mapGetters('profile', {
			activeProfile: 'activeProfile'
		})
	},
	components: {
		RecipeCard,
		ViewRecipe
	},
	watch: {
		activeProfile: function(val) {
			this.getRecipes()
		}
	},
	methods: {
		...mapActions('recipes', {
			getRecipes: 'getRecipes'
		})
	},

	created() {
		this.getRecipes()
		this.$emit('title', 'Pantry')
	}
}
</script>

<style scoped></style>
