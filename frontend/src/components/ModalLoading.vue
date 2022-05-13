<template>
	<div class="overlay">
		<div class="loading"></div>
	</div>
</template>

<script>
export default {
	name: 'ModalLoading'
}
</script>

<style lang="scss">
	.overlay {
		height: 100vh;
		width: 100vw;
		overflow: hidden;
		display: flex;
		justify-content: center;
		align-items: center;
		background: rgba(255, 255, 255, .6);
		background-size: cover;
		position: absolute;
		top: 0;
		left: 0;
		z-index: 20;
	}
	.loading {
		box-sizing: border-box;
		position: relative;
		--size: 60px;
		--color1: #ffd100;
		--color2: black;
		width: var(--size);
		height: var(--size);
		border-top: calc(var(--size) / 10) solid transparent;
		border-left: calc(var(--size) / 10) solid transparent;
		border-bottom: calc(var(--size) / 10) solid var(--color1);
		border-right: calc(var(--size) / 10) solid var(--color1);
		border-radius: 999px;
		transform: rotate(0);
		animation: anim__circle1-rotate 1s linear infinite;
	}
	.loading::after {
		position: absolute;
		content: "";
		---background-color: #00000033;
		width: var(--size);
		height: var(--size);
		border-bottom: calc(var(--size) / 10) solid var(--color2);
		border-right: calc(var(--size) / 10) solid var(--color2);
		border-left: calc(var(--size) / 10) solid transparent;
		border-top: calc(var(--size) / 10) solid transparent;
		border-radius: 999px;
		top: -25%;
		left: -25%;
		transform: rotate(0) scale(0.5);
		animation: anim__circle2-rotate 0.5s linear infinite;
	}
	@keyframes anim__circle1-rotate {
		to {
			transform: rotate(360deg);
		}
	}
	@keyframes anim__circle2-rotate {
		to {
			transform: rotate(-360deg) scale(0.5);
		}
	}
</style>
