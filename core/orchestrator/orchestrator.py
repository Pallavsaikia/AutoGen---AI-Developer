from core.agents.sk_agent import SKAgent

class Orchestrator:
    def __init__(self, router: SKAgent, developer: SKAgent, verifier: SKAgent, executor: SKAgent = None):
        self.router = router
        self.developer = developer
        self.verifier = verifier
        self.executor = executor

    async def route_task(self, input_text: str):
        """
        Start the orchestration flow where tasks are handled in iteration.
        """
        task_in_progress = True
        while task_in_progress:
            # Step 1: Router decides what needs to be done (Plan)
            routing_decision = await self.router.run(input_text)
            print(f"Routing decision: {routing_decision}")

            # Determine the action based on the routing decision
            if "coding" in routing_decision.lower():
                # Step 2: Developer writes the code
                print("Developer: Writing the code...")
                code = await self.developer.run(input_text)
                print(f"Code created: {code}")

                # Step 3: Verifier reviews the code
                print("Verifier: Reviewing the code...")
                review = await self.verifier.run(code)
                print(f"Code review: {review}")

                if review == "APPROVED":
                    # Step 4: Executor saves the code if approved
                    if self.executor:
                        print("Executor: Saving and executing the code...")
                        await self.executor.run(code)
                        return "Code executed and saved successfully."
                    else:
                        return "No executor available to execute the code."

                else:
                    return f"Code rejected: {review}"

            elif "verification" in routing_decision.lower():
                # If it's just verification, verify the existing code
                print("Verifier: Verifying the code...")
                review = await self.verifier.run(input_text)
                if review == "APPROVED":
                    return "Code verified and approved."
                else:
                    return f"Code rejected: {review}"
            
            elif "execution" in routing_decision.lower():
                # If it's an execution task, run the code
                print("Executor: Executing the code...")
                if self.executor:
                    await self.executor.run(input_text)
                    return "Code executed successfully."
                else:
                    return "No executor available for execution."

            else:
                # If the routing decision doesn't match any expected action, terminate the loop
                return "Unknown task type. Could not route."
            
            # Here, you can add logic for handling other possible stages if necessary
            # For example, you can break the loop based on some criteria or proceed to the next task.
