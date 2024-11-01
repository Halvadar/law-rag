<script>
  import { SignIn } from '@clerk/clerk-svelte';
</script>

<div class="login-container">
  <SignIn 
    path="/sign-in"
    routing="path"
    signUpUrl="/sign-up"
    afterSignInUrl="/"
    appearance={{
      elements: {
        formButtonPrimary: 'clerk-button',
        card: 'clerk-card',
        rootBox: 'clerk-root'
      }
    }}
  />
</div>

<style>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 1rem;
  }

  :global(.clerk-button) {
    background-color: #4CAF50 !important;
  }

  :global(.clerk-card) {
    border-radius: 8px !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
  }

  :global(.clerk-root) {
    width: 100% !important;
    max-width: 400px !important;
  }
</style>
