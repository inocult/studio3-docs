# Signal Mechanics

## The Technical Details of Belief and Doubt

<div class="arena-card">

<h3>⚙️ How Signals Actually Work</h3>

<p>Understanding the mechanics behind signaling is crucial for maximizing returns and minimizing risks. This guide covers the technical details, mathematical models, and strategic considerations of the signal system.</p>

</div>

## Signal Types Deep Dive

### Belief Signals

<div class="arena-card">

<h3>✅ Positive Conviction Mechanics</h3>

<p><strong>Technical Specifications:</strong></p>

<ul>
<li><strong>Minimum Stake:</strong> 10 $SIGNAL</li>
<li><strong>Maximum Stake:</strong> Based on reputation</li>
<li><strong>Lock Period:</strong> Until milestone completion</li>
<li><strong>Success Multiplier:</strong> 1.5x - 2.0x base</li>
<li><strong>Failure Result:</strong> 100% burn</li>
</ul>

<p><strong>Multiplier Formula:</strong></p>
<p>Your final multiplier is calculated by combining your base multiplier with various bonuses: time bonus (for early signals), reputation modifier (based on your XP), and phase factor (earlier phases have higher multipliers).</p>

</div>

### Doubt Signals

<div class="arena-card">

<h3>❌ Negative Conviction Mechanics</h3>


<p><strong>Technical Specifications:</strong></p>

<ul>
<li><strong>Minimum Stake:</strong> 10 $SIGNAL</li>
<li><strong>Maximum Stake:</strong> Based on reputation</li>
<li><strong>Lock Period:</strong> Until milestone completion</li>
<li><strong>Success Multiplier:</strong> 1.2x - 1.5x base</li>
<li><strong>Failure Result:</strong> 100% burn</li>
</ul>

<p><strong>Multiplier Formula:</strong></p>

<p>Your doubt signal multiplier combines the base rate with bonuses for going against the crowd (contrarian bonus), your track record of correct predictions (accuracy streak), and the overall risk level of the signal.</p>

</div>

## Multiplier System

### Base Multipliers

| Signal Type | Outcome | Base Range |
|------------|---------|------------|
| Belief | Success | 1.5x - 2.0x |
| Belief | Failure | 0x (burn) |
| Doubt | Success | 1.2x - 1.5x |
| Doubt | Failure | 0x (burn) |

### Bonus Modifiers

<div class="arena-card">

<h3>🎯 Multiplier Bonuses</h3>


<p><strong>Time Bonus (Early Signals):</strong></p>
<ul>
<li><strong>First 10% of pool:</strong> +0.5x</li>
<li>First 25% of pool: +0.3x</li>
<li>First 50% of pool: +0.1x</li>
<li>After 50%: No bonus</li>
</ul>

<p><strong>Reputation Modifier:</strong></p>
<ul>
<li><strong>0-100 XP:</strong> 1.0x</li>
<li>100-500 XP: 1.1x</li>
<li>500-2000 XP: 1.2x</li>
<li>2000+ XP: 1.3x</li>
</ul>

<p><strong>Phase Factor:</strong></p>
<ul>
<li><strong>Spark/Forge:</strong> 1.5x</li>
<li>Ignition: 1.3x</li>
<li>Drift: 1.2x</li>
<li>Orbit/Flare: 1.1x</li>
<li>Ascension: 1.0x</li>
</ul>
</div>

## Staking Mechanics

### The Staking Process

<div class="arena-card">

<h3>🔐 Technical Flow</h3>

<ol>
<li><strong>Signal Initiation</strong>
   <p>When you create a signal, the system automatically:</p>
   <ul>
   <li>Validates your stake amount meets requirements</li>
   <li>Checks that the venture is accepting signals</li>
   <li>Locks your tokens in a secure escrow</li>
   <li>Records your signal details on the blockchain</li>
   </ul>
</li>
<li><strong>Token Locking</strong>
<ul>
<li>Tokens transferred to escrow</li>
<li>Cannot be withdrawn</li>
<li>Tracked on-chain</li>
<li>Visible in UI</li>
</ul>
</li>
<li><strong>Settlement Trigger</strong>
<ul>
<li>Anchor validates milestone</li>
<li>Smart contract executes</li>
<li>Rewards calculated</li>
<li>Tokens distributed</li>
</ul>
</li>
</ol>
</div>

### Gas Optimization
<p><strong>Cost Considerations:</strong></p>
<ul>
<li><strong>Signal creation:</strong> ~50,000 gas</li>
<li><strong>Batch signals:</strong> ~30,000 gas each</li>
<li><strong>Claim rewards:</strong> ~80,000 gas</li>
<li><strong>Emergency exit:</strong> ~100,000 gas</li>
</ul>

<p><strong>Optimization Tips:</strong></p>
<ul>
<li><strong>Batch multiple signals</strong></li>
<li>Time for low gas periods</li>
<li>Use meta-transactions</li>
<li>Claim rewards together</li>
</ul>

## Pool Dynamics

### Signal Pool Mechanics

<div class="arena-card">

<h3>🏊 Pool Behavior</h3>
<p><strong>Pool Formation:</strong></p>
<ul>
<li><strong>Starts empty at milestone declaration</strong></li>
<li>Grows with each signal</li>
<li>Belief and doubt tracked separately</li>
<li>Ratio affects multipliers</li>
</ul>

<p><strong>Pool Metrics:</strong></p>
<p>The signal pool tracks three key metrics:</p>
<ul>
<li><strong>Total Pool:</strong> The sum of all belief and doubt stakes</li>
<li><strong>Belief Ratio:</strong> The percentage of the pool backing belief</li>
<li><strong>Sentiment:</strong> The overall community conviction (positive for more belief, negative for more doubt)</li>
</ul>

<p><strong>Dynamic Adjustments:</strong></p>
<ul>
<li><strong>High belief ratio → Lower belief multipliers</strong></li>
<li>High doubt ratio → Lower doubt multipliers</li>
<li>Balanced pools → Optimal returns</li>
<li>Extreme ratios → Contrarian opportunities</li>
</ul>
</div>

### Liquidity Considerations
<p><strong>Pool Depth Effects:</strong></p>
<ul>
<li><strong>Shallow pools:</strong> Higher volatility</li>
<li><strong>Deep pools:</strong> More stability</li>
<li><strong>Early signals:</strong> Price discovery</li>
<li><strong>Late signals:</strong> Efficient market</li>
</ul>

## Advanced Signal Types

### Conditional Signals

<div class="arena-card">

<h3>🔄 Complex Signaling</h3>
<p><strong>Types Available:</strong></p>

<ol>
<li><strong>Time-Conditional</strong>
<ul>
<li>"I believe IF completed by date X"</li>
<li>Different multipliers for time ranges</li>
<li>Partial rewards possible</li>
</ul>
</li>
<li><strong>Outcome-Conditional</strong>
<ul>
<li>"I believe IF metric Y achieved"</li>
<li>Specific success criteria</li>
<li>Binary or graduated rewards</li>
</ul>
</li>
<li><strong>Sequential Signals</strong>
<ul>
<li>Multi-milestone commitments</li>
<li>Compounding rewards</li>
<li>Higher risk/reward</li>
</ul>
</li>
</ol>
</div>

### Hedged Positions
<p><strong>Hedging Strategies:</strong></p>
<ul>
<li><strong>Belief + smaller doubt position</strong></li>
<li>Across similar ventures</li>
<li>Time-staggered entries</li>
<li>Phase diversification</li>
</ul>

## Signal Timing

### Optimal Entry Points

<div class="arena-card">

<h3>⏰ Timing Your Signals</h3>
<p><strong>Early Stage (0-20% filled):</strong></p>
<ul>
<li><strong>Pros:</strong> Maximum multipliers, first-mover advantage</li>
<li><strong>Cons:</strong> Limited information, high risk</li>
<li><strong>Best for:</strong> High-conviction plays</li>
</ul>

<p><strong>Growth Stage (20-60% filled):</strong></p>
<ul>
<li><strong>Pros:</strong> Some validation, decent multipliers</li>
<li><strong>Cons:</strong> Still significant risk</li>
<li><strong>Best for:</strong> Balanced approach</li>
</ul>

<p><strong>Late Stage (60-90% filled):</strong></p>
<ul>
<li><strong>Pros:</strong> Maximum information, lower risk</li>
<li><strong>Cons:</strong> Lower multipliers</li>
<li><strong>Best for:</strong> Risk-averse strategies</li>
</ul>

<p><strong>Final Stage (90-100% filled):</strong></p>
<ul>
<li><strong>Pros:</strong> Near-certain outcomes</li>
<li><strong>Cons:</strong> Minimal returns</li>
<li><strong>Best for:</strong> Safe accumulation</li>
</ul>
</div>

## Risk Calculations

### Mathematical Models

<div class="arena-card">

<h3>📊 Risk/Reward Analysis</h3>
<p><strong>Expected Value Formula:</strong></p>
<p>To calculate if a signal is worth making, consider your expected value: multiply your estimated success chance by your potential rewards, then subtract the risk of losing your stake. A positive expected value suggests a good opportunity.</p>

<p>**Example:**</p>

<p><strong>Calculation:</strong></p>
<ul>
<li><strong>Stake:</strong> 1,000 $SIGNAL</li>
<li>Success chance: 70%</li>
<li>Multiplier: 2.0x</li>
<li>EV = (0.7 × 2.0 × 1,000) - (0.3 × 1,000)</li>
<li>EV = 1,400 - 300 = 1,100 $SIGNAL</li>
</ul>

<p><strong>Break-even Success Rate:</strong></p>
<p>To profit from signals, you need a certain success rate based on the multiplier:</p>
<ul>
<li><strong>2.0x multiplier:</strong> You need at least 50% success rate to break even</li>
<li><strong>1.5x multiplier:</strong> You need at least 67% success rate to break even</li>
<li><strong>3.0x multiplier:</strong> You need at least 33% success rate to break even</li>
</ul>
<p>Higher multipliers mean you can afford more failures while still profiting.</p>

</div>

### Portfolio Risk Management


<p><strong>Optimal Allocation:</strong></p>
<ul>
<li><strong>No single signal > 10% of bankroll</strong></li>
<li>Phase diversification</li>
<li>Venture diversification</li>
<li>Belief/doubt balance</li>
</ul>

## Settlement Process

### How Rewards Distribute

<div class="arena-card">

<h3>💰 Settlement Mechanics</h3>
<p><strong>Success Settlement:</strong></p>
<ol>
<li>Anchor validates success</li>
<li>Smart contract triggered</li>
<li>Doubt stakes burned</li>
<li>Belief rewards calculated</li>
<li>Tokens distributed</li>
<li>XP awarded</li>
</ol>

<p><strong>Failure Settlement:</strong></p>
<ol>
<li>Anchor validates failure</li>
<li>Smart contract triggered</li>
<li>Belief stakes burned</li>
<li>Doubt rewards calculated</li>
<li>Tokens distributed</li>
<li>XP adjusted</li>
</ol>

</div>

### Emergency Procedures
<p><strong>Force Exit Conditions:</strong></p>
<ul>
<li><strong>Venture abandonment</strong></li>
<li>Smart contract issues</li>
<li>Governance intervention</li>
<li>Extended delays</li>
</ul>

<p><strong>Emergency Exit Cost:</strong></p>
<ul>
<li><strong>90% token return</strong></li>
<li>10% penalty burn</li>
<li>No XP gained/lost</li>
<li>Reputation impact</li>
</ul>

## Gas and Fees

### Transaction Costs

<div class="arena-card">

<h3>⛽ Fee Structure</h3>
<p><strong>Platform Fees:</strong></p>
<ul>
<li><strong>Signal creation:</strong> 0.5% of stake</li>
<li>Reward claim: 1% of profit</li>
<li>Emergency exit: 10% penalty</li>
<li>No maintenance fees</li>
</ul>

<p><strong>Network Fees:</strong></p>
<ul>
<li><strong>Vary by congestion</strong></li>
<li>~$5-50 per transaction</li>
<li>Batch for savings</li>
<li>Time for low periods</li>
</ul>
</div>

## Technical Integration

### API Access
<p><strong>Available Endpoints:</strong></p>
<p>The platform provides several ways to interact with signals programmatically:</p>
<ul>
<li><strong>View your signals:</strong> Access your complete signal history and active positions</li>
<li><strong>Check venture signals:</strong> See all signals for a specific venture</li>
<li><strong>Create new signals:</strong> Submit belief or doubt signals through the API</li>
<li><strong>Track signal status:</strong> Monitor the real-time status of your signals</li>
</ul>

### Smart Contract Interface


<p><strong>Key Functions:</strong></p>
<p>The smart contract provides these main functions:</p>
<ul>
<li><strong>Create Signal:</strong> Submit a new belief or doubt signal with your chosen stake amount</li>
<li><strong>Claim Rewards:</strong> Collect your earnings after successful milestone completion</li>
<li><strong>Emergency Exit:</strong> Withdraw your stake early with a 10% penalty in special circumstances</li>
<li><strong>Get Signal Details:</strong> View complete information about any signal</li>
</ul>

## Monitoring Tools

### Signal Tracking

<div class="arena-card">

<h3>📈 Performance Monitoring</h3>
<p><strong>Dashboard Metrics:</strong></p>
<ul>
<li><strong>Active signals status</strong></li>
<li>Pending settlements</li>
<li>Historical performance</li>
<li>ROI calculations</li>
<li>Risk exposure</li>
</ul>

<p><strong>Alert System:</strong></p>
<ul>
<li><strong>Milestone deadlines</strong></li>
<li>Settlement notifications</li>
<li>Pool movements</li>
<li>Opportunity alerts</li>
</ul>
</div>

## Advanced Strategies

### Arbitrage Opportunities
<p><strong>Types of Arbitrage:</strong></p>
<ul>
<li><strong>Cross-venture similar milestones</strong></li>
<li>Time-based mispricings</li>
<li>Information asymmetry</li>
<li>Sentiment extremes</li>
</ul>

### Algorithmic Signaling
<p><strong>Automated Strategies:</strong></p>
<ul>
<li><strong>Rule-based entries</strong></li>
<li>Portfolio rebalancing</li>
<li>Risk management</li>
<li>Sentiment following</li>
</ul>

## Common Technical Issues

### Troubleshooting

<div class="arena-card">

<h3>🔧 Problem Resolution</h3>
<p><strong>Transaction Failures:</strong></p>
<ul>
<li><strong>Insufficient gas</strong></li>
<li>Token approval needed</li>
<li>Pool limits reached</li>
<li>Network congestion</li>
</ul>

<p><strong>Settlement Delays:</strong></p>
<ul>
<li><strong>Anchor queue</strong></li>
<li>Dispute process</li>
<li>Technical issues</li>
<li>Governance votes</li>
</ul>
</div>

## Next Steps

### Deepen Your Knowledge

Continue with:

1. [Rewards System](rewards-system.md) - Detailed reward structures
2. [Due Diligence Framework](due-diligence.md) - Analysis methods
3. [Risk Management](risk-management.md) - Advanced protection

---

!!! info "Technical Note"
    Signal mechanics are continuously optimized based on ecosystem data. Stay updated with the latest parameters through official channels.

!!! warning "Risk Reminder"
    Understanding mechanics doesn't guarantee profits. Always signal within your risk tolerance and never invest more than you can afford to lose.