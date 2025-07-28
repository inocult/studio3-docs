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

<p>**Technical Specifications:**</p>

<ul>
<li>**Minimum Stake:** 10 $SIGNAL</li>
</ul>
<p>-- **Maximum Stake:**</p>

<p>**Lock Period:**</p>
<p>-- **Success Multiplier:**</p>

<p>**Failure Result:**</p>
<p>**  Multiplier Formula:**</p>
```
<p>Base Multiplier × Time Bonus × Reputation Modifier × Phase Factor</p>
```

</div>

### Doubt Signals

<div class="arena-card">

<h3>❌ Negative Conviction Mechanics</h3>


<p>Technical Specifications:**</p>
<ul>
<li>**Minimum Stake:** 10 $SIGNAL</li>
</ul>
<p>-- **Maximum Stake:**</p>

<p>**Lock Period:**</p>
<p>-- **Success Multiplier:**</p>

<p>**Failure Result:**</p>
<p>**  Multiplier Formula:**</p>
```
<p>Base Multiplier × Contrarian Bonus × Accuracy Streak × Risk Factor</p>
```

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


<p>Time Bonus (Early Signals):**</p>
<ul>
<li>**First 10% of pool: +0.5x**</li>
<li>First 25% of pool: +0.3x</li>
<li>First 50% of pool: +0.1x</li>
<li>After 50%: No bonus</li>

</ul>
<p>** Reputation Modifier:**</p>
<ul>
<li>**0-100 XP: 1.0x**</li>
<li>100-500 XP: 1.1x</li>
<li>500-2000 XP: 1.2x</li>
<li>2000+ XP: 1.3x</li>

</ul>
<p>** Phase Factor:**</p>
<ul>
<li>**Spark/Forge: 1.5x**</li>
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

<p>1. **Signal Initiation**</p>
   ```javascript
<p>function createSignal(ventureId, signalType, amount) {</p>
<p>validateStake(amount);</p>
<p>checkVentureStatus(ventureId);</p>
<p>lockTokens(msg.sender, amount);</p>
<p>recordSignal(signalDetails);</p>
<p>}</p>
   ```

<p>2. **Token Locking**</p>

<ul>
<li>Tokens transferred to escrow</li>

<li>Cannot be withdrawn</li>
<li>Tracked on</li>
<li>chain</li>

<li>Visible in UI</li>

</ul>
<p>3. **Settlement Trigger**</p>

<ul>
<li>Anchor validates milestone</li>

<li>Smart contract executes</li>

<li>Rewards calculated</li>

<li>Tokens distributed</li>

</ul>
</div>

### Gas Optimization
** Cost Considerations:**
- **Signal creation: ~50,000 gas**
- Batch signals: ~30,000 gas each
- Claim rewards: ~80,000 gas
- Emergency exit: ~100,000 gas

** Optimization Tips:**
- **Batch multiple signals**
- Time for low gas periods
- Use meta-transactions
- Claim rewards together

## Pool Dynamics

### Signal Pool Mechanics

<div class="arena-card">

<h3>🏊 Pool Behavior</h3>
<p>** Pool Formation:**</p>
<ul>
<li>**Starts empty at milestone declaration**</li>
<li>Grows with each signal</li>
<li>Belief and doubt tracked separately</li>
<li>Ratio affects multipliers</li>

</ul>
<p>** Pool Metrics:**</p>
```
<p>Total Pool = Belief Stakes + Doubt Stakes</p>
<p>Belief Ratio = Belief Stakes / Total Pool</p>
<p>Sentiment = (Belief - Doubt) / Total Pool</p>
```



<p>Dynamic Adjustments:**</p>
<ul>
<li>**High belief ratio → Lower belief multipliers**</li>
<li>High doubt ratio → Lower doubt multipliers</li>
<li>Balanced pools → Optimal returns</li>
<li>Extreme ratios → Contrarian opportunities</li>

</ul>
</div>

### Liquidity Considerations
** Pool Depth Effects:**
- **Shallow pools: Higher volatility**
- Deep pools: More stability
- Early signals: Price discovery
- Late signals: Efficient market

## Advanced Signal Types

### Conditional Signals

<div class="arena-card">

<h3>🔄 Complex Signaling</h3>
<p>** Types Available:**</p>
<p>1. **Time-Conditional**</p>

<ul>
<li>"I believe IF completed by date X"</li>

<li>Different multipliers for time ranges</li>

<li>Partial rewards possible</li>

</ul>
<p>2. **Outcome-Conditional**</p>

<ul>
<li>"I believe IF metric Y achieved"</li>

<li>Specific success criteria</li>

<li>Binary or graduated rewards</li>

</ul>
<p>3. **Sequential Signals**</p>
<ul>
<li>Multi</li>
<li>milestone commitments</li>

<li>Compounding rewards</li>

<li>Higher risk/reward</li>

</ul>
</div>

### Hedged Positions
** Hedging Strategies:**
- **Belief + smaller doubt position**
- Across similar ventures
- Time-staggered entries
- Phase diversification

## Signal Timing

### Optimal Entry Points

<div class="arena-card">

<h3>⏰ Timing Your Signals</h3>
<p>** Early Stage (0-20% filled):**</p>
<ul>
<li>**Pros:**</li>

</ul>
<p>**Maximum multipliers, first-mover advantage**</p>
<p>-- **Cons:**</p>

<p>**Best for:**</p>
<ul>
<li>**Growth Stage (20-60% filled):**</li>

</ul>
<p>**Some validation, decent multipliers**</p>
<p>-- **Cons:**</p>

<p>**Best for:**</p>
<ul>
<li>**Late Stage (60-90% filled):**</li>

</ul>
<p>**Maximum information, lower risk**</p>
<p>-- **Cons:**</p>

<p>**Best for:**</p>
<ul>
<li>**Final Stage (90-100% filled):**</li>

</ul>
<p>**Near-certain outcomes**</p>
<p>-- **Cons:**</p>

<p>**Best for:**</p>
</div>

## Risk Calculations

### Mathematical Models

<div class="arena-card">

<h3>📊 Risk/Reward Analysis</h3>
<p>** Expected Value Formula:**</p>
```
<p>EV = (Success Probability × Reward Multiplier × Stake) -</p>
<p>(Failure Probability × Stake)</p>
```

<p>**Example:**</p>

<p>**Calculation:**</p>
<ul>
<li>**Stake: 1,000 $SIGNAL**</li>
<li>Success chance: 70%</li>
<li>Multiplier: 2.0x</li>
<li>EV = (0.7 × 2.0 × 1,000)</li>
<li>(0.3 × 1,000)</li>
<li>EV = 1,400</li>
<li>300 = 1,100 $SIGNAL</li>

</ul>
<p>** Break-even Success Rate:**</p>
```
<p>Break-even = 1 / Multiplier</p>
<p>2. 0x multiplier = 50% success needed</p>
<p>1. 5x multiplier = 67% success needed</p>
<p>3. 0x multiplier = 33% success needed</p>
```

</div>

### Portfolio Risk Management


Optimal Allocation:**
- **No single signal > 10% of bankroll**
- Phase diversification
- Venture diversification
- Belief/doubt balance

## Settlement Process

### How Rewards Distribute

<div class="arena-card">

<h3>💰 Settlement Mechanics</h3>
<p>** Success Settlement:**</p>
<p>1. Anchor validates success</p>
<p>2. Smart contract triggered</p>
<p>3. Doubt stakes burned</p>
<p>4. Belief rewards calculated</p>
<p>5. Tokens distributed</p>
<p>6. XP awarded</p>



<p>Failure Settlement:**</p>
<p>1. Anchor validates failure</p>
<p>2. Smart contract triggered</p>
<p>3. Belief stakes burned</p>
<p>4. Doubt rewards calculated</p>
<p>5. Tokens distributed</p>
<p>6. XP adjusted</p>

</div>

### Emergency Procedures
** Force Exit Conditions:**
- **Venture abandonment**
- Smart contract issues
- Governance intervention
- Extended delays

** Emergency Exit Cost:**
- **90% token return**
- 10% penalty burn
- No XP gained/lost
- Reputation impact

## Gas and Fees

### Transaction Costs

<div class="arena-card">

<h3>⛽ Fee Structure</h3>
<p>** Platform Fees:**</p>
<ul>
<li>**Signal creation: 0.5% of stake**</li>
<li>Reward claim: 1% of profit</li>
<li>Emergency exit: 10% penalty</li>
<li>No maintenance fees</li>

</ul>
<p>** Network Fees:**</p>
<ul>
<li>**Vary by congestion**</li>
<li>~$5-50 per transaction</li>
<li>Batch for savings</li>
<li>Time for low periods</li>

</ul>
</div>

## Technical Integration

### API Access
** Available Endpoints:**
```javascript
GET /api/signals/{userId} - Your signals
GET /api/ventures/{ventureId}/signals - Venture signals
POST /api/signals/create - Create signal
GET /api/signals/{signalId}/status - Check status
```

### Smart Contract Interface


Key Functions:**
```solidity
createSignal(uint ventureId, bool belief, uint amount)
claimRewards(uint signalId)
emergencyExit(uint signalId)
getSignalDetails(uint signalId)
```

## Monitoring Tools

### Signal Tracking

<div class="arena-card">

<h3>📈 Performance Monitoring</h3>
<p>** Dashboard Metrics:**</p>
<ul>
<li>**Active signals status**</li>
<li>Pending settlements</li>
<li>Historical performance</li>
<li>ROI calculations</li>
<li>Risk exposure</li>

</ul>
<p>** Alert System:**</p>
<ul>
<li>**Milestone deadlines**</li>
<li>Settlement notifications</li>
<li>Pool movements</li>
<li>Opportunity alerts</li>

</ul>
</div>

## Advanced Strategies

### Arbitrage Opportunities
** Types of Arbitrage:**
- **Cross-venture similar milestones**
- Time-based mispricings
- Information asymmetry
- Sentiment extremes

### Algorithmic Signaling
** Automated Strategies:**
- **Rule-based entries**
- Portfolio rebalancing
- Risk management
- Sentiment following

## Common Technical Issues

### Troubleshooting

<div class="arena-card">

<h3>🔧 Problem Resolution</h3>
<p>** Transaction Failures:**</p>
<ul>
<li>**Insufficient gas**</li>
<li>Token approval needed</li>
<li>Pool limits reached</li>
<li>Network congestion</li>

</ul>
<p>** Settlement Delays:**</p>
<ul>
<li>**Anchor queue**</li>
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